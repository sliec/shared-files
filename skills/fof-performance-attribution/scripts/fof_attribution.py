#!/usr/bin/env python3
"""
FOF业绩归因与绩效分析计算脚本
用法：
  python fof_attribution.py brinson --input holdings.xlsx --benchmark benchmark.xlsx
  python fof_attribution.py factor  --input nav.csv --factors factors.csv --rf rf.csv
  python fof_attribution.py timing  --input nav.csv --market market.csv --rf rf.csv
  python fof_attribution.py risk    --input nav.csv --rf rf.csv
  python fof_attribution.py full    --input nav.csv --holdings holdings.xlsx --factors factors.csv --market market.csv --rf rf.csv --benchmark benchmark.xlsx
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
# Brinson 归因
# ============================================================

def brinson_single_period(holdings_df, benchmark_df):
    """
    单期Brinson归因
    
    holdings_df: DataFrame，列=[category, weight_p, return_p]
    benchmark_df: DataFrame，列=[category, weight_b, return_b]
    
    返回: dict {AA, SS, IA, total_excess, details}
    """
    merged = holdings_df.merge(benchmark_df, on='category', how='outer').fillna(0)
    
    wp = merged['weight_p'].values
    wb = merged['weight_b'].values
    rp = merged['return_p'].values
    rb = merged['return_b'].values
    
    rp_total = np.sum(wp * rp)
    rb_total = np.sum(wb * rb)
    
    # 资产配置效应
    aa = np.sum((wp - wb) * rb)
    # 基金选择效应
    ss = np.sum(wb * (rp - rb))
    # 交互效应
    ia = np.sum((wp - wb) * (rp - rb))
    
    # 各类别明细
    details = []
    for i, row in merged.iterrows():
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
        'AA': round(aa, 6),
        'SS': round(ss, 6),
        'IA': round(ia, 6),
        'total_excess': round(rp_total - rb_total, 6),
        'portfolio_return': round(rp_total, 6),
        'benchmark_return': round(rb_total, 6),
        'details': details
    }


def carino_linking(period_results):
    """
    Carino多期联结算法
    period_results: list of 单期归因结果
    """
    total_rp = np.prod([1 + p['portfolio_return'] for p in period_results]) - 1
    total_rb = np.prod([1 + p['benchmark_return'] for p in period_results]) - 1
    
    total_aa, total_ss, total_ia = 0, 0, 0
    
    for p in period_results:
        rp_t = p['portfolio_return']
        rb_t = p['benchmark_return']
        
        if abs(rp_t - rb_t) > 1e-10:
            a_t = (rp_t - rb_t) / (np.log(1 + rp_t) - np.log(1 + rb_t))
        else:
            a_t = 1.0
        
        total_aa += a_t * p['AA']
        total_ss += a_t * p['SS']
        total_ia += a_t * p['IA']
    
    return {
        'AA': round(total_aa, 6),
        'SS': round(total_ss, 6),
        'IA': round(total_ia, 6),
        'total_excess': round(total_aa + total_ss + total_ia, 6),
        'portfolio_return': round(total_rp, 6),
        'benchmark_return': round(total_rb, 6),
        'linking_method': 'Carino'
    }


# ============================================================
# 多因子回归归因
# ============================================================

def factor_regression(fund_excess, factor_df, model_type='carhart'):
    """
    多因子回归
    
    fund_excess: Series, 基金超额收益率
    factor_df: DataFrame, 因子收益率 (columns: market, smb, hml, mom)
    model_type: 'capm', 'ff3', 'carhart'
    """
    X_parts = [factor_df['market']]
    
    if model_type in ('ff3', 'carhart'):
        X_parts.append(factor_df['smb'])
        X_parts.append(factor_df['hml'])
    
    if model_type == 'carhart':
        X_parts.append(factor_df['mom'])
    
    X = pd.concat(X_parts, axis=1)
    X = sm.add_constant(X)
    
    # 对齐
    common_idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[common_idx]
    X = X.loc[common_idx]
    
    model = sm.OLS(y, X).fit()
    
    # 年化Alpha（假设周频 ×52，日频 ×252）
    n_periods = len(common_idx)
    if n_periods > 200:
        annualize = 252  # 日频
    elif n_periods > 40:
        annualize = 52   # 周频
    else:
        annualize = 12   # 月频
    
    result = {
        'model': model_type,
        'alpha': round(model.params['const'], 6),
        'alpha_annualized': round(model.params['const'] * annualize, 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'r_squared': round(model.rsquared, 4),
        'adj_r_squared': round(model.rsquared_adj, 4),
        'n_obs': n_periods,
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
    """
    滚动Alpha计算
    window: 滚动窗口长度（默认126天=半年）
    """
    alphas = []
    dates = []
    
    for i in range(window, len(fund_excess)):
        y_window = fund_excess.iloc[i-window:i]
        X_window = factor_df.iloc[i-window:i]
        
        try:
            result, _ = factor_regression(y_window, X_window, model_type)
            alphas.append(result['alpha_annualized'])
            dates.append(fund_excess.index[i])
        except:
            alphas.append(np.nan)
            dates.append(fund_excess.index[i])
    
    return pd.Series(alphas, index=dates, name='rolling_alpha')


# ============================================================
# 择时能力检验
# ============================================================

def treynor_mazuy(fund_excess, market_excess):
    """
    T-M模型择时检验
    R_p - R_f = α + b(R_m - R_f) + c(R_m - R_f)² + ε
    """
    market_sq = market_excess ** 2
    X = pd.DataFrame({
        'market': market_excess.values,
        'market_sq': market_sq.values
    }, index=market_excess.index)
    
    common_idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[common_idx]
    X = sm.add_constant(X.loc[common_idx])
    
    model = sm.OLS(y, X).fit()
    
    return {
        'model': 'Treynor-Mazuy',
        'alpha': round(model.params['const'], 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'beta_market': round(model.params['market'], 4),
        'beta_market_pvalue': round(model.pvalues['market'], 4),
        'gamma_timing': round(model.params['market_sq'], 6),
        'gamma_pvalue': round(model.pvalues['market_sq'], 4),
        'has_timing': model.params['market_sq'] > 0 and model.pvalues['market_sq'] < 0.1,
        'timing_significance': '显著' if model.pvalues['market_sq'] < 0.05 else ('边缘显著' if model.pvalues['market_sq'] < 0.1 else '不显著'),
        'r_squared': round(model.rsquared, 4),
    }


def henriksson_merton(fund_excess, market_excess):
    """
    H-M模型择时检验
    R_p - R_f = α + b(R_m - R_f) + d·D·(R_m - R_f) + ε
    D = 1 if R_m > R_f else 0
    """
    bull = (market_excess > 0).astype(float)
    interaction = bull * market_excess
    
    X = pd.DataFrame({
        'market': market_excess.values,
        'interaction': interaction.values
    }, index=market_excess.index)
    
    common_idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[common_idx]
    X = sm.add_constant(X.loc[common_idx])
    
    model = sm.OLS(y, X).fit()
    
    return {
        'model': 'Henriksson-Merton',
        'alpha': round(model.params['const'], 6),
        'alpha_pvalue': round(model.pvalues['const'], 4),
        'beta_bear': round(model.params['market'], 4),
        'beta_bear_pvalue': round(model.pvalues['market'], 4),
        'delta_timing': round(model.params['interaction'], 4),
        'delta_pvalue': round(model.pvalues['interaction'], 4),
        'beta_bull': round(model.params['market'] + model.params['interaction'], 4),
        'has_timing': model.params['interaction'] > 0 and model.pvalues['interaction'] < 0.1,
        'timing_significance': '显著' if model.pvalues['interaction'] < 0.05 else ('边缘显著' if model.pvalues['interaction'] < 0.1 else '不显著'),
        'r_squared': round(model.rsquared, 4),
    }


# ============================================================
# 风险收益指标
# ============================================================

def risk_return_metrics(returns, rf_returns=None, periods_per_year=252):
    """
    计算全套风险收益指标
    
    returns: Series, 基金收益率序列
    rf_returns: Series, 无风险利率序列（可选，默认0）
    periods_per_year: 年化频率（252日/52周/12月）
    """
    if rf_returns is None:
        rf_returns = pd.Series(0, index=returns.index)
    
    excess = returns - rf_returns
    
    # 年化收益
    total_return = (1 + returns).prod() - 1
    n_years = len(returns) / periods_per_year
    ann_return = (1 + total_return) ** (1 / n_years) - 1 if n_years > 0 else 0
    
    # 年化波动
    ann_vol = returns.std() * np.sqrt(periods_per_year)
    
    # 年化超额收益
    ann_excess = excess.mean() * periods_per_year
    
    # 夏普比率
    sharpe = ann_excess / ann_vol if ann_vol > 0 else 0
    
    # 最大回撤
    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    max_dd = drawdown.min()
    
    # 卡玛比率
    calmar = ann_return / abs(max_dd) if max_dd != 0 else 0
    
    # 索提诺比率
    downside = excess[excess < 0]
    downside_std = downside.std() * np.sqrt(periods_per_year) if len(downside) > 0 else 0
    sortino = ann_excess / downside_std if downside_std > 0 else 0
    
    # 回撤恢复天数
    dd_end = drawdown.idxmin()
    recovery_date = None
    if dd_end is not None:
        post_dd = cum_returns[dd_end:]
        peak_before_dd = cum_returns[:dd_end].max() if len(cum_returns[:dd_end]) > 0 else cum_returns.iloc[0]
        recovered = post_dd[post_dd >= peak_before_dd]
        if len(recovered) > 0:
            recovery_date = recovered.index[0]
    
    return {
        'total_return': round(total_return, 6),
        'annualized_return': round(ann_return, 6),
        'annualized_volatility': round(ann_vol, 6),
        'sharpe_ratio': round(sharpe, 4),
        'max_drawdown': round(max_dd, 6),
        'max_drawdown_date': str(drawdown.idxmin().date()) if drawdown.idxmin() is not None else None,
        'calmar_ratio': round(calmar, 4),
        'sortino_ratio': round(sortino, 4),
        'recovery_date': str(recovery_date.date()) if recovery_date is not None else '未恢复',
        'n_observations': len(returns),
        'n_years': round(n_years, 2),
    }


def information_ratio(fund_returns, benchmark_returns, periods_per_year=252):
    """
    信息比率
    """
    excess = fund_returns - benchmark_returns
    tracking_error = excess.std() * np.sqrt(periods_per_year)
    ann_excess = excess.mean() * periods_per_year
    
    ir = ann_excess / tracking_error if tracking_error > 0 else 0
    
    return {
        'information_ratio': round(ir, 4),
        'annualized_excess': round(ann_excess, 6),
        'tracking_error': round(tracking_error, 6),
    }


# ============================================================
# 基金经理能力综合评级
# ============================================================

def ability_rating(factor_result, tm_result, hm_result, risk_metrics):
    """
    五维能力评级
    """
    ratings = {}
    
    # 1. 选基能力
    alpha = factor_result.get('alpha_annualized', 0)
    alpha_p = factor_result.get('alpha_pvalue', 1)
    if alpha > 0.02 and alpha_p < 0.05:
        ratings['selection'] = {'level': '卓越', 'stars': 5}
    elif alpha > 0.01 and alpha_p < 0.1:
        ratings['selection'] = {'level': '优秀', 'stars': 4}
    elif alpha > 0 and alpha_p < 0.2:
        ratings['selection'] = {'level': '合格', 'stars': 3}
    elif alpha_p < 0.3:
        ratings['selection'] = {'level': '待观察', 'stars': 2}
    else:
        ratings['selection'] = {'level': '不足', 'stars': 1}
    ratings['selection']['detail'] = f"Carhart Alpha={alpha:.2%}(年化), p={alpha_p:.3f}"
    
    # 2. 择时能力
    tm_has = tm_result.get('has_timing', False)
    hm_has = hm_result.get('has_timing', False)
    if tm_has and hm_has:
        ratings['timing'] = {'level': '优秀', 'stars': 4}
    elif tm_has or hm_has:
        ratings['timing'] = {'level': '合格', 'stars': 3}
    else:
        tm_sig = tm_result.get('timing_significance', '不显著')
        if '边缘' in tm_sig:
            ratings['timing'] = {'level': '待观察', 'stars': 2}
        else:
            ratings['timing'] = {'level': '不足', 'stars': 1}
    ratings['timing']['detail'] = f"T-M: {tm_result.get('timing_significance', 'N/A')}, H-M: {hm_result.get('timing_significance', 'N/A')}"
    
    # 3. 风控能力
    mdd = abs(risk_metrics.get('max_drawdown', 0))
    calmar = risk_metrics.get('calmar_ratio', 0)
    if mdd < 0.05 and calmar > 2:
        ratings['risk_control'] = {'level': '卓越', 'stars': 5}
    elif mdd < 0.10 and calmar > 1:
        ratings['risk_control'] = {'level': '优秀', 'stars': 4}
    elif mdd < 0.15:
        ratings['risk_control'] = {'level': '合格', 'stars': 3}
    elif mdd < 0.25:
        ratings['risk_control'] = {'level': '待观察', 'stars': 2}
    else:
        ratings['risk_control'] = {'level': '不足', 'stars': 1}
    ratings['risk_control']['detail'] = f"最大回撤={mdd:.2%}, 卡玛={calmar:.2f}"
    
    # 4. 综合评级
    avg_stars = np.mean([r['stars'] for r in ratings.values()])
    if avg_stars >= 4:
        overall = '卓越'
    elif avg_stars >= 3.5:
        overall = '优秀'
    elif avg_stars >= 2.5:
        overall = '合格'
    elif avg_stars >= 1.5:
        overall = '待观察'
    else:
        overall = '不建议'
    
    return {
        'ratings': ratings,
        'overall': overall,
        'avg_stars': round(avg_stars, 1),
    }


# ============================================================
# CLI入口
# ============================================================

def load_csv(path, index_col=0, parse_dates=True):
    df = pd.read_csv(path, index_col=index_col, parse_dates=parse_dates)
    return df

def main():
    parser = argparse.ArgumentParser(description='FOF业绩归因分析工具')
    subparsers = parser.add_subparsers(dest='command')
    
    # Brinson
    p_brinson = subparsers.add_parser('brinson', help='Brinson归因分析')
    p_brinson.add_argument('--input', required=True, help='持仓数据文件(Excel/CSV)')
    p_brinson.add_argument('--benchmark', required=True, help='基准数据文件(Excel/CSV)')
    
    # Factor regression
    p_factor = subparsers.add_parser('factor', help='多因子回归归因')
    p_factor.add_argument('--input', required=True, help='FOF净值文件(CSV)')
    p_factor.add_argument('--factors', required=True, help='因子数据文件(CSV)')
    p_factor.add_argument('--rf', help='无风险利率文件(CSV)')
    p_factor.add_argument('--model', default='carhart', choices=['capm', 'ff3', 'carhart'])
    
    # Timing
    p_timing = subparsers.add_parser('timing', help='择时能力检验')
    p_timing.add_argument('--input', required=True, help='FOF净值文件(CSV)')
    p_timing.add_argument('--market', required=True, help='市场收益率文件(CSV)')
    p_timing.add_argument('--rf', help='无风险利率文件(CSV)')
    
    # Risk metrics
    p_risk = subparsers.add_parser('risk', help='风险收益指标')
    p_risk.add_argument('--input', required=True, help='FOF净值文件(CSV)')
    p_risk.add_argument('--rf', help='无风险利率文件(CSV)')
    p_risk.add_argument('--freq', default='daily', choices=['daily', 'weekly', 'monthly'])
    
    # Full analysis
    p_full = subparsers.add_parser('full', help='完整分析')
    p_full.add_argument('--input', required=True, help='FOF净值文件(CSV)')
    p_full.add_argument('--holdings', help='持仓数据文件')
    p_full.add_argument('--factors', help='因子数据文件(CSV)')
    p_full.add_argument('--market', help='市场收益率文件(CSV)')
    p_full.add_argument('--rf', help='无风险利率文件(CSV)')
    p_full.add_argument('--benchmark', help='基准数据文件')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    freq_map = {'daily': 252, 'weekly': 52, 'monthly': 12}
    
    if args.command == 'brinson':
        if args.input.endswith('.xlsx'):
            holdings = pd.read_excel(args.input)
        else:
            holdings = pd.read_csv(args.input)
        if args.benchmark.endswith('.xlsx'):
            benchmark = pd.read_excel(args.benchmark)
        else:
            benchmark = pd.read_csv(args.benchmark)
        result = brinson_single_period(holdings, benchmark)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == 'factor':
        nav = load_csv(args.input)
        factors = load_csv(args.factors)
        rf = load_csv(args.rf) if args.rf else None
        
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf_ret = rf.iloc[:, 0] / 252 if rf is not None else pd.Series(0, index=returns.index)
        fund_excess = returns - rf_ret
        
        result, model = factor_regression(fund_excess, factors, args.model)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == 'timing':
        nav = load_csv(args.input)
        market = load_csv(args.market)
        rf = load_csv(args.rf) if args.rf else None
        
        returns = nav.iloc[:, 0].pct_change().dropna()
        mkt_ret = market.iloc[:, 0]
        rf_ret = rf.iloc[:, 0] / 252 if rf is not None else pd.Series(0, index=returns.index)
        
        fund_excess = returns - rf_ret
        market_excess = mkt_ret - rf_ret
        
        tm = treynor_mazuy(fund_excess, market_excess)
        hm = henriksson_merton(fund_excess, market_excess)
        
        print("=== T-M模型 ===")
        print(json.dumps(tm, ensure_ascii=False, indent=2))
        print("\n=== H-M模型 ===")
        print(json.dumps(hm, ensure_ascii=False, indent=2))
    
    elif args.command == 'risk':
        nav = load_csv(args.input)
        rf = load_csv(args.rf) if args.rf else None
        
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf_ret = rf.iloc[:, 0] / freq_map[args.freq] if rf is not None else None
        
        metrics = risk_return_metrics(returns, rf_ret, freq_map[args.freq])
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
    
    elif args.command == 'full':
        nav = load_csv(args.input)
        returns = nav.iloc[:, 0].pct_change().dropna()
        
        rf = load_csv(args.rf) if args.rf else None
        rf_ret = rf.iloc[:, 0] / 252 if rf is not None else pd.Series(0, index=returns.index)
        fund_excess = returns - rf_ret
        
        results = {}
        
        # 风险指标
        results['risk_metrics'] = risk_return_metrics(returns, rf_ret if rf is not None else None)
        
        # 因子回归
        if args.factors:
            factors = load_csv(args.factors)
            factor_res, _ = factor_regression(fund_excess, factors, 'carhart')
            results['factor_regression'] = factor_res
        else:
            factor_res = {'alpha_annualized': 0, 'alpha_pvalue': 1}
            results['factor_regression'] = factor_res
        
        # 择时检验
        if args.market:
            market = load_csv(args.market)
            mkt_ret = market.iloc[:, 0]
            market_excess = mkt_ret - rf_ret
            tm = treynor_mazuy(fund_excess, market_excess)
            hm = henriksson_merton(fund_excess, market_excess)
        else:
            tm = {'has_timing': False, 'timing_significance': '未检验'}
            hm = {'has_timing': False, 'timing_significance': '未检验'}
        results['timing_tm'] = tm
        results['timing_hm'] = hm
        
        # Brinson（如有持仓）
        if args.holdings and args.benchmark:
            if args.holdings.endswith('.xlsx'):
                holdings = pd.read_excel(args.holdings)
            else:
                holdings = pd.read_csv(args.holdings)
            if args.benchmark.endswith('.xlsx'):
                benchmark = pd.read_excel(args.benchmark)
            else:
                benchmark = pd.read_csv(args.benchmark)
            results['brinson'] = brinson_single_period(holdings, benchmark)
        
        # 综合评级
        results['ability_rating'] = ability_rating(
            factor_res, tm, hm, results['risk_metrics']
        )
        
        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
