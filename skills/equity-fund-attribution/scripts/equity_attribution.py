#!/usr/bin/env python3
"""
权益类基金业绩归因与绩效分析计算脚本
用法：
  python equity_attribution.py factor   --input nav.csv --factors factors.csv [--rf rf.csv] [--model carhart]
  python equity_attribution.py timing   --input nav.csv --market market.csv [--rf rf.csv]
  python equity_attribution.py brinson  --input holdings.xlsx --benchmark benchmark.xlsx
  python equity_attribution.py risk     --input nav.csv [--rf rf.csv] [--freq daily]
  python equity_attribution.py risk-attr --exposures exposures.csv --covar covar_matrix.csv
  python equity_attribution.py ability  --input nav.csv --factors factors.csv --market market.csv [--rf rf.csv]
  python equity_attribution.py full     --input nav.csv --holdings holdings.xlsx --factors factors.csv --market market.csv [--rf rf.csv] --benchmark benchmark.xlsx
"""

import argparse
import sys
import json
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

try:
    import statsmodels.api as sm
except ImportError:
    print("请安装 statsmodels: pip install statsmodels")
    sys.exit(1)


# ============================================================
# 净值法：多因子回归
# ============================================================

def factor_regression(fund_excess, factor_df, model_type='carhart'):
    """
    多因子回归：CAPM / FF3 / Carhart / FF5
    """
    X_parts = [factor_df['market']]

    if model_type in ('ff3', 'carhart', 'ff5'):
        X_parts.append(factor_df['smb'])
        X_parts.append(factor_df['hml'])

    if model_type == 'carhart':
        X_parts.append(factor_df['mom'])

    if model_type == 'ff5':
        X_parts.append(factor_df['rmw'])
        X_parts.append(factor_df['cma'])

    X = pd.concat(X_parts, axis=1)
    X = sm.add_constant(X)

    common_idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[common_idx]
    X = X.loc[common_idx]

    model = sm.OLS(y, X).fit()

    # 年化Alpha
    n = len(common_idx)
    if n > 200:
        ann = 252
    elif n > 40:
        ann = 52
    else:
        ann = 12

    result = {
        'model': model_type,
        'alpha': round(model.params['const'], 6),
        'alpha_annualized': round(model.params['const'] * ann, 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'r_squared': round(model.rsquared, 4),
        'adj_r_squared': round(model.rsquared_adj, 4),
        'n_obs': n,
        'coefficients': {},
    }

    for col in X.columns:
        if col != 'const':
            result['coefficients'][col] = {
                'beta': round(model.params[col], 4),
                't_stat': round(model.tvalues[col], 4),
                'p_value': round(model.pvalues[col], 4),
            }

    return result, model


def rolling_alpha(fund_excess, factor_df, model_type='carhart', window=126):
    """滚动Alpha（默认半年窗口=126交易日）"""
    alphas, dates = [], []
    for i in range(window, len(fund_excess)):
        y_w = fund_excess.iloc[i-window:i]
        X_w = factor_df.iloc[i-window:i]
        try:
            res, _ = factor_regression(y_w, X_w, model_type)
            alphas.append(res['alpha_annualized'])
        except:
            alphas.append(np.nan)
        dates.append(fund_excess.index[i])
    return pd.Series(alphas, index=dates, name='rolling_alpha')


def style_drift_detection(fund_excess, factor_df, window=126):
    """风格漂移检测：滚动因子暴露的波动度"""
    betas = {col: [] for col in factor_df.columns if col != 'const'}

    for i in range(window, len(fund_excess)):
        y_w = fund_excess.iloc[i-window:i]
        X_w = factor_df.iloc[i-window:i]
        try:
            _, model = factor_regression(y_w, X_w, 'carhart')
            for col in betas:
                betas[col].append(model.params.get(col, np.nan))
        except:
            for col in betas:
                betas[col].append(np.nan)

    drift = {}
    for col, vals in betas.items():
        s = pd.Series(vals).dropna()
        drift[col] = {
            'mean': round(s.mean(), 4),
            'std': round(s.std(), 4),
            'cv': round(s.std() / abs(s.mean()), 4) if abs(s.mean()) > 0.001 else float('inf'),
            'trend': 'stable' if s.std() < 0.3 else ('drifting' if s.std() < 0.6 else 'unstable'),
        }

    return drift


# ============================================================
# 选股-择时能力模型（T-M / H-M / C-L）
# ============================================================

def treynor_mazuy(fund_excess, market_excess):
    """T-M模型"""
    market_sq = market_excess ** 2
    X = pd.DataFrame({
        'market': market_excess.values,
        'market_sq': market_sq.values
    }, index=market_excess.index)

    idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[idx]
    X = sm.add_constant(X.loc[idx])
    model = sm.OLS(y, X).fit()

    return {
        'model': 'Treynor-Mazuy',
        'alpha': round(model.params['const'], 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'beta_market': round(model.params['market'], 4),
        'gamma_timing': round(model.params['market_sq'], 6),
        'gamma_pvalue': round(model.pvalues['market_sq'], 4),
        'has_timing': model.params['market_sq'] > 0 and model.pvalues['market_sq'] < 0.1,
        'has_selection': model.params['const'] > 0 and model.pvalues['const'] < 0.1,
        'timing_sig': _sig(model.pvalues['market_sq']),
        'selection_sig': _sig(model.pvalues['const']),
        'r_squared': round(model.rsquared, 4),
    }


def henriksson_merton(fund_excess, market_excess):
    """H-M模型"""
    bull = (market_excess > 0).astype(float)
    interaction = bull * market_excess

    X = pd.DataFrame({
        'market': market_excess.values,
        'interaction': interaction.values
    }, index=market_excess.index)

    idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[idx]
    X = sm.add_constant(X.loc[idx])
    model = sm.OLS(y, X).fit()

    return {
        'model': 'Henriksson-Merton',
        'alpha': round(model.params['const'], 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'beta_bear': round(model.params['market'], 4),
        'delta_timing': round(model.params['interaction'], 4),
        'delta_pvalue': round(model.pvalues['interaction'], 4),
        'beta_bull': round(model.params['market'] + model.params['interaction'], 4),
        'has_timing': model.params['interaction'] > 0 and model.pvalues['interaction'] < 0.1,
        'has_selection': model.params['const'] > 0 and model.pvalues['const'] < 0.1,
        'timing_sig': _sig(model.pvalues['interaction']),
        'selection_sig': _sig(model.pvalues['const']),
        'r_squared': round(model.rsquared, 4),
    }


def chang_lewellen(fund_excess, market_excess):
    """C-L模型"""
    bull = (market_excess > 0).astype(float)
    interaction = bull * market_excess

    X = pd.DataFrame({
        'market': market_excess.values,
        'interaction': interaction.values
    }, index=market_excess.index)

    idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[idx]
    X = sm.add_constant(X.loc[idx])
    model = sm.OLS(y, X).fit()

    b1 = model.params['market']
    b2 = model.params['interaction']
    timing_score = b1 - b2

    return {
        'model': 'Chang-Lewellen',
        'alpha': round(model.params['const'], 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'beta1': round(b1, 4),
        'beta2': round(b2, 4),
        'beta1_pvalue': round(model.pvalues['market'], 4),
        'beta2_pvalue': round(model.pvalues['interaction'], 4),
        'timing_score': round(timing_score, 4),
        'has_timing': timing_score > 0 and model.pvalues['interaction'] < 0.1,
        'has_selection': model.params['const'] > 0 and model.pvalues['const'] < 0.1,
        'timing_sig': _sig(model.pvalues['interaction']),
        'selection_sig': _sig(model.pvalues['const']),
        'r_squared': round(model.rsquared, 4),
    }


def _sig(p):
    if p < 0.01: return '高度显著'
    if p < 0.05: return '显著'
    if p < 0.10: return '边缘显著'
    return '不显著'


# ============================================================
# Brinson持仓归因
# ============================================================

def brinson_single_period(holdings_df, benchmark_df, scheme='BF'):
    """
    单期Brinson归因
    scheme: 'BHB'（交互单独列示）或 'BF'（交互归入配置）
    """
    merged = holdings_df.merge(benchmark_df, on='category', how='outer').fillna(0)

    wp = merged['weight_p'].values
    wb = merged['weight_b'].values
    rp = merged['return_p'].values
    rb = merged['return_b'].values

    rp_total = np.sum(wp * rp)
    rb_total = np.sum(wb * rb)

    aa = np.sum((wp - wb) * rb)
    ss = np.sum(wb * (rp - rb))
    ia = np.sum((wp - wb) * (rp - rb))

    if scheme == 'BF':
        aa += ia
        ia = 0.0

    details = []
    for _, row in merged.iterrows():
        details.append({
            'category': row['category'],
            'weight_p': round(row['weight_p'], 4),
            'weight_b': round(row['weight_b'], 4),
            'return_p': round(row['return_p'], 4),
            'return_b': round(row['return_b'], 4),
            'AA': round((row['weight_p'] - row['weight_b']) * row['return_b'], 6),
            'SS': round(row['weight_b'] * (row['return_p'] - row['return_b']), 6),
            'IA': round((row['weight_p'] - row['weight_b']) * (row['return_p'] - row['return_b']), 6),
        })

    return {
        'scheme': scheme,
        'AA': round(aa, 6),
        'SS': round(ss, 6),
        'IA': round(ia, 6),
        'total_excess': round(rp_total - rb_total, 6),
        'portfolio_return': round(rp_total, 6),
        'benchmark_return': round(rb_total, 6),
        'details': details
    }


def carino_linking(period_results):
    """Carino多期无残差联结"""
    total_rp = np.prod([1 + p['portfolio_return'] for p in period_results]) - 1
    total_rb = np.prod([1 + p['benchmark_return'] for p in period_results]) - 1

    total_aa, total_ss, total_ia = 0, 0, 0
    for p in period_results:
        rp_t, rb_t = p['portfolio_return'], p['benchmark_return']
        if abs(rp_t - rb_t) > 1e-10:
            a_t = (rp_t - rb_t) / (np.log(1 + rp_t) - np.log(1 + rb_t))
        else:
            a_t = 1.0
        total_aa += a_t * p['AA']
        total_ss += a_t * p['SS']
        total_ia += a_t * p['IA']

    return {
        'AA': round(total_aa, 6), 'SS': round(total_ss, 6), 'IA': round(total_ia, 6),
        'total_excess': round(total_aa + total_ss + total_ia, 6),
        'portfolio_return': round(total_rp, 6),
        'benchmark_return': round(total_rb, 6),
        'linking_method': 'Carino'
    }


# ============================================================
# 风险收益指标
# ============================================================

def risk_return_metrics(returns, rf_returns=None, periods_per_year=252):
    """全套风险收益指标"""
    if rf_returns is None:
        rf_returns = pd.Series(0, index=returns.index)

    excess = returns - rf_returns
    total_return = (1 + returns).prod() - 1
    n_years = len(returns) / periods_per_year
    ann_return = (1 + total_return) ** (1 / max(n_years, 0.01)) - 1

    ann_vol = returns.std() * np.sqrt(periods_per_year)
    ann_excess = excess.mean() * periods_per_year
    sharpe = ann_excess / ann_vol if ann_vol > 0 else 0

    cum = (1 + returns).cumprod()
    rolling_max = cum.cummax()
    dd = (cum - rolling_max) / rolling_max
    max_dd = dd.min()

    calmar = ann_return / abs(max_dd) if max_dd != 0 else 0

    downside = excess[excess < 0]
    ds_std = downside.std() * np.sqrt(periods_per_year) if len(downside) > 0 else 0
    sortino = ann_excess / ds_std if ds_std > 0 else 0

    return {
        'total_return': round(total_return, 6),
        'annualized_return': round(ann_return, 6),
        'annualized_volatility': round(ann_vol, 6),
        'sharpe_ratio': round(sharpe, 4),
        'max_drawdown': round(max_dd, 6),
        'max_drawdown_date': str(dd.idxmin().date()) if dd.idxmin() is not None else None,
        'calmar_ratio': round(calmar, 4),
        'sortino_ratio': round(sortino, 4),
        'treynor_ratio': round(ann_excess / 1.0, 4),  # needs beta
        'n_observations': len(returns),
        'n_years': round(n_years, 2),
    }


def information_ratio(fund_returns, benchmark_returns, periods_per_year=252):
    """信息比率"""
    excess = fund_returns - benchmark_returns
    te = excess.std() * np.sqrt(periods_per_year)
    ann_excess = excess.mean() * periods_per_year
    ir = ann_excess / te if te > 0 else 0
    return {
        'information_ratio': round(ir, 4),
        'annualized_excess': round(ann_excess, 6),
        'tracking_error': round(te, 6),
    }


# ============================================================
# 风险归因（x-sigma-rho）
# ============================================================

def risk_attribution_xsr(exposures, factor_returns, factor_cov=None):
    """
    x-sigma-rho风险归因
    exposures: Series, 各因子暴露度
    factor_returns: DataFrame, 各因子历史收益
    factor_cov: DataFrame, 因子协方差矩阵（可选，自动计算）
    """
    if factor_cov is None:
        factor_cov = factor_returns.cov() * 252

    factor_std = np.sqrt(np.diag(factor_cov))
    portfolio_var = exposures.values @ factor_cov.values @ exposures.values
    portfolio_std = np.sqrt(portfolio_var) if portfolio_var > 0 else 1e-10

    # 因子收益与组合收益的相关性
    port_returns = factor_returns @ exposures.values
    correlations = factor_returns.corrwith(port_returns)

    results = []
    for i, factor in enumerate(exposures.index):
        x = exposures.iloc[i]
        sigma = factor_std[i]
        rho = correlations.get(factor, 0)
        risk_contrib = abs(x * sigma * rho)

        results.append({
            'factor': factor,
            'exposure': round(x, 4),
            'volatility': round(sigma, 6),
            'correlation': round(rho, 4),
            'risk_contribution': round(risk_contrib, 6),
            'risk_pct': round(risk_contrib / portfolio_std * 100, 2),
        })

    results.sort(key=lambda r: r['risk_contribution'], reverse=True)
    return {
        'portfolio_volatility': round(portfolio_std, 6),
        'factor_contributions': results,
    }


# ============================================================
# 能力圈综合评级
# ============================================================

def ability_rating(factor_result, tm_result, hm_result, cl_result, risk_metrics):
    """六维能力评级"""
    ratings = {}

    # 1. 选股能力
    alpha = factor_result.get('alpha_annualized', 0)
    alpha_p = factor_result.get('alpha_pvalue', 1)
    if alpha > 0.03 and alpha_p < 0.05:
        ratings['selection'] = {'level': '卓越', 'stars': 5}
    elif alpha > 0.02 and alpha_p < 0.05:
        ratings['selection'] = {'level': '优秀', 'stars': 4}
    elif alpha > 0 and alpha_p < 0.1:
        ratings['selection'] = {'level': '合格', 'stars': 3}
    elif alpha_p < 0.3:
        ratings['selection'] = {'level': '待观察', 'stars': 2}
    else:
        ratings['selection'] = {'level': '不足', 'stars': 1}
    ratings['selection']['detail'] = f"Carhart α={alpha:.2%}(年化), p={alpha_p:.3f}"

    # 2. 择时能力
    tm_ok = tm_result.get('has_timing', False)
    hm_ok = hm_result.get('has_timing', False)
    cl_ok = cl_result.get('has_timing', False)
    timing_count = sum([tm_ok, hm_ok, cl_ok])
    if timing_count >= 2:
        ratings['timing'] = {'level': '优秀', 'stars': 4}
    elif timing_count == 1:
        ratings['timing'] = {'level': '合格', 'stars': 3}
    else:
        any_marginal = any('边缘' in r.get('timing_sig', '') for r in [tm_result, hm_result, cl_result])
        ratings['timing'] = {'level': '待观察' if any_marginal else '不足', 'stars': 2 if any_marginal else 1}
    ratings['timing']['detail'] = f"T-M:{tm_result.get('timing_sig','N/A')}, H-M:{hm_result.get('timing_sig','N/A')}, C-L:{cl_result.get('timing_sig','N/A')}"

    # 3. 风控能力
    mdd = abs(risk_metrics.get('max_drawdown', 0))
    calmar = risk_metrics.get('calmar_ratio', 0)
    if mdd < 0.10 and calmar > 2:
        ratings['risk_control'] = {'level': '卓越', 'stars': 5}
    elif mdd < 0.15 and calmar > 1:
        ratings['risk_control'] = {'level': '优秀', 'stars': 4}
    elif mdd < 0.25:
        ratings['risk_control'] = {'level': '合格', 'stars': 3}
    elif mdd < 0.35:
        ratings['risk_control'] = {'level': '待观察', 'stars': 2}
    else:
        ratings['risk_control'] = {'level': '不足', 'stars': 1}
    ratings['risk_control']['detail'] = f"最大回撤={mdd:.2%}, 卡玛={calmar:.2f}"

    # 综合
    avg = np.mean([r['stars'] for r in ratings.values()])
    overall = '卓越' if avg >= 4 else ('优秀' if avg >= 3.5 else ('合格' if avg >= 2.5 else ('待观察' if avg >= 1.5 else '不建议')))

    return {'ratings': ratings, 'overall': overall, 'avg_stars': round(avg, 1)}


# ============================================================
# CLI
# ============================================================

def load_csv(path, index_col=0, parse_dates=True):
    return pd.read_csv(path, index_col=index_col, parse_dates=parse_dates)

def main():
    parser = argparse.ArgumentParser(description='权益类基金业绩归因分析工具')
    sub = parser.add_subparsers(dest='cmd')

    # factor
    p = sub.add_parser('factor')
    p.add_argument('--input', required=True)
    p.add_argument('--factors', required=True)
    p.add_argument('--rf')
    p.add_argument('--model', default='carhart', choices=['capm', 'ff3', 'carhart', 'ff5'])

    # timing
    p = sub.add_parser('timing')
    p.add_argument('--input', required=True)
    p.add_argument('--market', required=True)
    p.add_argument('--rf')

    # brinson
    p = sub.add_parser('brinson')
    p.add_argument('--input', required=True)
    p.add_argument('--benchmark', required=True)
    p.add_argument('--scheme', default='BF', choices=['BHB', 'BF'])

    # risk
    p = sub.add_parser('risk')
    p.add_argument('--input', required=True)
    p.add_argument('--rf')
    p.add_argument('--freq', default='daily', choices=['daily', 'weekly', 'monthly'])

    # risk-attr
    p = sub.add_parser('risk-attr')
    p.add_argument('--exposures', required=True)
    p.add_argument('--factor-returns', required=True)

    # ability
    p = sub.add_parser('ability')
    p.add_argument('--input', required=True)
    p.add_argument('--factors', required=True)
    p.add_argument('--market', required=True)
    p.add_argument('--rf')

    # full
    p = sub.add_parser('full')
    p.add_argument('--input', required=True)
    p.add_argument('--holdings')
    p.add_argument('--factors')
    p.add_argument('--market')
    p.add_argument('--rf')
    p.add_argument('--benchmark')

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    freq_map = {'daily': 252, 'weekly': 52, 'monthly': 12}

    if args.cmd == 'factor':
        nav = load_csv(args.input)
        factors = load_csv(args.factors)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        result, _ = factor_regression(returns - rf, factors, args.model)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == 'timing':
        nav = load_csv(args.input)
        market = load_csv(args.market)
        returns = nav.iloc[:, 0].pct_change().dropna()
        mkt = market.iloc[:, 0]
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        fe = returns - rf
        me = mkt - rf

        print("=== T-M模型 ===")
        print(json.dumps(treynor_mazuy(fe, me), ensure_ascii=False, indent=2))
        print("\n=== H-M模型 ===")
        print(json.dumps(henriksson_merton(fe, me), ensure_ascii=False, indent=2))
        print("\n=== C-L模型 ===")
        print(json.dumps(chang_lewellen(fe, me), ensure_ascii=False, indent=2))

    elif args.cmd == 'brinson':
        h = pd.read_excel(args.input) if args.input.endswith('.xlsx') else pd.read_csv(args.input)
        b = pd.read_excel(args.benchmark) if args.benchmark.endswith('.xlsx') else pd.read_csv(args.benchmark)
        result = brinson_single_period(h, b, args.scheme)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == 'risk':
        nav = load_csv(args.input)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / freq_map[args.freq] if args.rf else None
        print(json.dumps(risk_return_metrics(returns, rf, freq_map[args.freq]), ensure_ascii=False, indent=2))

    elif args.cmd == 'risk-attr':
        exp = pd.read_csv(args.exposures, index_col=0).iloc[:, 0]
        fr = load_csv(args.factor_returns)
        result = risk_attribution_xsr(exp, fr)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == 'ability':
        nav = load_csv(args.input)
        factors = load_csv(args.factors)
        market = load_csv(args.market)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        fe = returns - rf
        me = market.iloc[:, 0] - rf

        fr, _ = factor_regression(fe, factors, 'carhart')
        tm = treynor_mazuy(fe, me)
        hm = henriksson_merton(fe, me)
        cl = chang_lewellen(fe, me)
        rr = risk_return_metrics(returns, rf if args.rf else None)

        rating = ability_rating(fr, tm, hm, cl, rr)
        result = {
            'factor_regression': fr,
            'timing_tm': tm, 'timing_hm': hm, 'timing_cl': cl,
            'risk_metrics': rr,
            'ability_rating': rating,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    elif args.cmd == 'full':
        nav = load_csv(args.input)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        fe = returns - rf

        results = {'risk_metrics': risk_return_metrics(returns, rf if args.rf else None)}

        if args.factors:
            factors = load_csv(args.factors)
            fr, _ = factor_regression(fe, factors, 'carhart')
            results['factor_regression'] = fr
        else:
            fr = {'alpha_annualized': 0, 'alpha_pvalue': 1}
            results['factor_regression'] = fr

        if args.market:
            me = load_csv(args.market).iloc[:, 0] - rf
            tm = treynor_mazuy(fe, me)
            hm = henriksson_merton(fe, me)
            cl = chang_lewellen(fe, me)
        else:
            tm = {'has_timing': False, 'timing_sig': '未检验'}
            hm = {'has_timing': False, 'timing_sig': '未检验'}
            cl = {'has_timing': False, 'timing_sig': '未检验'}
        results['timing_tm'] = tm
        results['timing_hm'] = hm
        results['timing_cl'] = cl

        if args.holdings and args.benchmark:
            h = pd.read_excel(args.holdings) if args.holdings.endswith('.xlsx') else pd.read_csv(args.holdings)
            b = pd.read_excel(args.benchmark) if args.benchmark.endswith('.xlsx') else pd.read_csv(args.benchmark)
            results['brinson'] = brinson_single_period(h, b)

        results['ability_rating'] = ability_rating(fr, tm, hm, cl, results['risk_metrics'])
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
