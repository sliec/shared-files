#!/usr/bin/env python3
"""
固收类基金业绩归因与绩效分析计算脚本
用法：
  python fixed_income_attribution.py campisi    --input holdings.csv --benchmark benchmark.csv
  python fixed_income_attribution.py factor     --input nav.csv --factors factors.csv [--rf rf.csv]
  python fixed_income_attribution.py brinson    --input holdings.xlsx --benchmark benchmark.xlsx
  python fixed_income_attribution.py timing     --input nav.csv --stock-market market.csv --bond-market bond.csv [--rf rf.csv]
  python fixed_income_attribution.py risk       --input nav.csv [--rf rf.csv] [--freq daily]
  python fixed_income_attribution.py pnl        --input income_statement.csv
  python fixed_income_attribution.py full       --input nav.csv --holdings holdings.csv --factors factors.csv --stock-market market.csv --bond-market bond.csv [--rf rf.csv] --benchmark benchmark.csv
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
# Campisi 持仓归因（纯债归因核心）
# ============================================================

def campisi_attribution(fund_holdings, benchmark_holdings):
    """
    Campisi四效应模型
    fund_holdings / benchmark_holdings: DataFrame
      columns: [bond_id, weight, coupon_rate, mod_duration, ytm_start, ytm_end, rf_start, rf_end, spread_start, spread_end]
    """
    def compute_effects(df):
        w = df['weight'].values
        coupon = df['coupon_rate'].values
        dur = df['mod_duration'].values
        dy_rf = (df['rf_end'] - df['rf_start']).values
        dy_spread = (df['spread_end'] - df['spread_start']).values

        income = np.sum(w * coupon)
        treasury = np.sum(w * (-dur) * dy_rf)
        spread = np.sum(w * (-dur) * dy_spread)
        total = np.sum(w * (coupon + (-dur) * (dy_rf + dy_spread)))
        selection = total - income - treasury - spread

        return {
            'income_effect': round(float(income), 6),
            'treasury_effect': round(float(treasury), 6),
            'spread_effect': round(float(spread), 6),
            'selection_effect': round(float(selection), 6),
            'total_return': round(float(total), 6),
        }

    fund_effects = compute_effects(fund_holdings)
    bench_effects = compute_effects(benchmark_holdings)

    excess = {}
    for key in ['income_effect', 'treasury_effect', 'spread_effect', 'selection_effect']:
        excess[key] = round(fund_effects[key] - bench_effects[key], 6)
    excess['total_excess'] = round(sum(excess.values()), 6)

    return {
        'fund_effects': fund_effects,
        'benchmark_effects': bench_effects,
        'excess_attribution': excess,
    }


# ============================================================
# 净值法：Campisi五因子回归
# ============================================================

def campisi_factor_regression(fund_excess, factor_df):
    """
    Campisi五因子回归
    factor_df columns: [duration, curve, credit, default, equity]
    """
    cols = [c for c in ['duration', 'curve', 'credit', 'default', 'equity'] if c in factor_df.columns]
    X = factor_df[cols]
    X = sm.add_constant(X)

    idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[idx]
    X = X.loc[idx]

    model = sm.OLS(y, X).fit()

    n = len(idx)
    ann = 252 if n > 200 else (52 if n > 40 else 12)

    result = {
        'alpha': round(float(model.params['const']), 6),
        'alpha_annualized': round(float(model.params['const'] * ann), 6),
        'alpha_pvalue': round(float(model.pvalues['const']), 4),
        'r_squared': round(float(model.rsquared), 4),
        'adj_r_squared': round(float(model.rsquared_adj), 4),
        'n_obs': n,
        'coefficients': {},
    }

    for col in cols:
        result['coefficients'][col] = {
            'beta': round(float(model.params[col]), 4),
            't_stat': round(float(model.tvalues[col]), 4),
            'p_value': round(float(model.pvalues[col]), 4),
        }

    return result, model


# ============================================================
# 财报法（利润表拆解）
# ============================================================

def pnl_decomposition(income_df):
    """
    利润表拆解
    income_df: DataFrame with columns:
      [interest_income, investment_income, fair_value_change, other_income,
       bond_interest, bond_investment, bond_fv, stock_investment, stock_fv]
    """
    row = income_df.iloc[0] if len(income_df) > 0 else income_df

    total = (row.get('interest_income', 0) + row.get('investment_income', 0)
             + row.get('fair_value_change', 0) + row.get('other_income', 0))

    result = {
        'total_profit': round(float(total), 2),
        'components': {
            'interest_income': round(float(row.get('interest_income', 0)), 2),
            'investment_income': round(float(row.get('investment_income', 0)), 2),
            'fair_value_change': round(float(row.get('fair_value_change', 0)), 2),
            'other_income': round(float(row.get('other_income', 0)), 2),
        },
    }

    if total != 0:
        for k, v in result['components'].items():
            result['components'][f'{k}_pct'] = round(v / total * 100, 2)

    # "固收+"拆分
    bond_part = (row.get('bond_interest', 0) + row.get('bond_investment', 0)
                 + row.get('bond_fv', 0))
    stock_part = (row.get('stock_investment', 0) + row.get('stock_fv', 0))

    if bond_part + stock_part > 0:
        result['asset_contribution'] = {
            'bond_contribution': round(float(bond_part), 2),
            'stock_contribution': round(float(stock_part), 2),
            'bond_pct': round(bond_part / (bond_part + stock_part) * 100, 2),
            'stock_pct': round(stock_part / (bond_part + stock_part) * 100, 2),
        }

    return result


# ============================================================
# Brinson归因（"固收+"多资产）
# ============================================================

def brinson_attribution(holdings_df, benchmark_df, scheme='BF'):
    """Brinson归因"""
    merged = holdings_df.merge(benchmark_df, on='category', how='outer').fillna(0)
    wp = merged['weight_p'].values
    wb = merged['weight_b'].values
    rp = merged['return_p'].values
    rb = merged['return_b'].values

    aa = np.sum((wp - wb) * rb)
    ss = np.sum(wb * (rp - rb))
    ia = np.sum((wp - wb) * (rp - rb))

    if scheme == 'BF':
        aa += ia
        ia = 0.0

    return {
        'scheme': scheme,
        'AA': round(float(aa), 6),
        'SS': round(float(ss), 6),
        'IA': round(float(ia), 6),
        'total_excess': round(float(np.sum(wp * rp) - np.sum(wb * rb)), 6),
    }


# ============================================================
# 择时能力检验（双市场T-M模型）
# ============================================================

def dual_market_timing(fund_excess, stock_excess, bond_excess):
    """
    双市场T-M模型（股票+债券择时）
    """
    stock_sq = stock_excess ** 2
    bond_sq = bond_excess ** 2

    X = pd.DataFrame({
        'stock': stock_excess.values,
        'bond': bond_excess.values,
        'stock_sq': stock_sq.values,
        'bond_sq': bond_sq.values,
    }, index=stock_excess.index)

    idx = fund_excess.index.intersection(X.index)
    y = fund_excess.loc[idx]
    X = sm.add_constant(X.loc[idx])
    model = sm.OLS(y, X).fit()

    def _sig(p):
        if p < 0.01: return 'highly significant'
        if p < 0.05: return 'significant'
        if p < 0.10: return 'marginally significant'
        return 'not significant'

    return {
        'alpha': round(float(model.params['const']), 6),
        'alpha_pvalue': round(float(model.pvalues['const']), 4),
        'beta_stock': round(float(model.params['stock']), 4),
        'beta_bond': round(float(model.params['bond']), 4),
        'gamma_stock_timing': round(float(model.params['stock_sq']), 6),
        'gamma_stock_pvalue': round(float(model.pvalues['stock_sq']), 4),
        'gamma_bond_timing': round(float(model.params['bond_sq']), 6),
        'gamma_bond_pvalue': round(float(model.pvalues['bond_sq']), 4),
        'stock_timing': model.params['stock_sq'] > 0 and model.pvalues['stock_sq'] < 0.1,
        'bond_timing': model.params['bond_sq'] > 0 and model.pvalues['bond_sq'] < 0.1,
        'stock_timing_sig': _sig(model.pvalues['stock_sq']),
        'bond_timing_sig': _sig(model.pvalues['bond_sq']),
        'r_squared': round(float(model.rsquared), 4),
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

    # 固收特有：创新高占比、涨跌收益比
    up_days = (returns > 0).sum()
    total_days = len(returns)
    win_ratio = up_days / total_days if total_days > 0 else 0

    up_avg = returns[returns > 0].mean() if up_days > 0 else 0
    down_avg = abs(returns[returns < 0].mean()) if (total_days - up_days) > 0 else 1e-10
    profit_loss_ratio = up_avg / down_avg

    return {
        'total_return': round(float(total_return), 6),
        'annualized_return': round(float(ann_return), 6),
        'annualized_volatility': round(float(ann_vol), 6),
        'sharpe_ratio': round(float(sharpe), 4),
        'max_drawdown': round(float(max_dd), 6),
        'calmar_ratio': round(float(calmar), 4),
        'sortino_ratio': round(float(sortino), 4),
        'win_ratio_daily': round(float(win_ratio), 4),
        'profit_loss_ratio': round(float(profit_loss_ratio), 4),
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
        'information_ratio': round(float(ir), 4),
        'annualized_excess': round(float(ann_excess), 6),
        'tracking_error': round(float(te), 6),
    }


# ============================================================
# CLI
# ============================================================

def load_csv(path, index_col=0, parse_dates=True):
    return pd.read_csv(path, index_col=index_col, parse_dates=parse_dates)


def main():
    parser = argparse.ArgumentParser(description='固收类基金业绩归因分析工具')
    sub = parser.add_subparsers(dest='cmd')

    p = sub.add_parser('campisi')
    p.add_argument('--input', required=True)
    p.add_argument('--benchmark', required=True)

    p = sub.add_parser('factor')
    p.add_argument('--input', required=True)
    p.add_argument('--factors', required=True)
    p.add_argument('--rf')

    p = sub.add_parser('brinson')
    p.add_argument('--input', required=True)
    p.add_argument('--benchmark', required=True)
    p.add_argument('--scheme', default='BF', choices=['BHB', 'BF'])

    p = sub.add_parser('timing')
    p.add_argument('--input', required=True)
    p.add_argument('--stock-market', required=True)
    p.add_argument('--bond-market', required=True)
    p.add_argument('--rf')

    p = sub.add_parser('risk')
    p.add_argument('--input', required=True)
    p.add_argument('--rf')
    p.add_argument('--freq', default='daily', choices=['daily', 'weekly', 'monthly'])

    p = sub.add_parser('pnl')
    p.add_argument('--input', required=True)

    p = sub.add_parser('full')
    p.add_argument('--input', required=True)
    p.add_argument('--holdings')
    p.add_argument('--factors')
    p.add_argument('--stock-market')
    p.add_argument('--bond-market')
    p.add_argument('--rf')
    p.add_argument('--benchmark')

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    freq_map = {'daily': 252, 'weekly': 52, 'monthly': 12}

    if args.cmd == 'campisi':
        fund = pd.read_csv(args.input)
        bench = pd.read_csv(args.benchmark)
        print(json.dumps(campisi_attribution(fund, bench), ensure_ascii=False, indent=2))

    elif args.cmd == 'factor':
        nav = load_csv(args.input)
        factors = load_csv(args.factors)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        result, _ = campisi_factor_regression(returns - rf, factors)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == 'brinson':
        h = pd.read_excel(args.input) if args.input.endswith('.xlsx') else pd.read_csv(args.input)
        b = pd.read_excel(args.benchmark) if args.benchmark.endswith('.xlsx') else pd.read_csv(args.benchmark)
        print(json.dumps(brinson_attribution(h, b, args.scheme), ensure_ascii=False, indent=2))

    elif args.cmd == 'timing':
        nav = load_csv(args.input)
        stock_mkt = load_csv(args.stock_market)
        bond_mkt = load_csv(args.bond_market)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        fe = returns - rf
        se = stock_mkt.iloc[:, 0] - rf
        be = bond_mkt.iloc[:, 0] - rf
        print(json.dumps(dual_market_timing(fe, se, be), ensure_ascii=False, indent=2))

    elif args.cmd == 'risk':
        nav = load_csv(args.input)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / freq_map[args.freq] if args.rf else None
        print(json.dumps(risk_return_metrics(returns, rf, freq_map[args.freq]), ensure_ascii=False, indent=2))

    elif args.cmd == 'pnl':
        df = pd.read_csv(args.input)
        print(json.dumps(pnl_decomposition(df), ensure_ascii=False, indent=2))

    elif args.cmd == 'full':
        nav = load_csv(args.input)
        returns = nav.iloc[:, 0].pct_change().dropna()
        rf = load_csv(args.rf).iloc[:, 0] / 252 if args.rf else pd.Series(0, index=returns.index)
        fe = returns - rf

        results = {'risk_metrics': risk_return_metrics(returns, rf if args.rf else None)}

        if args.factors:
            factors = load_csv(args.factors)
            fr, _ = campisi_factor_regression(fe, factors)
            results['campisi_regression'] = fr

        if args.stock_market and args.bond_market:
            se = load_csv(args.stock_market).iloc[:, 0] - rf
            be = load_csv(args.bond_market).iloc[:, 0] - rf
            results['dual_market_timing'] = dual_market_timing(fe, se, be)

        if args.holdings and args.benchmark:
            h = pd.read_csv(args.holdings)
            b = pd.read_csv(args.benchmark)
            results['campisi_attribution'] = campisi_attribution(h, b)

        print(json.dumps(results, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
