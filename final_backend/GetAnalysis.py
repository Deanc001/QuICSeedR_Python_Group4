import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, mannwhitneyu, trim_mean


def get_analysis(calculation_spread, control, test='wilcox', alternative='two-sided', adjust_p=False, alpha=0.05):
    calculation_spread = {term: df.rename(columns=str) for term, df in calculation_spread.items()}

    def err_t_test(x, y, alternative='two-sided'):
        x, y = x.dropna(), y.dropna()
        try:
            return ttest_ind(x, y, alternative=alternative)
        except ValueError:
            return None

    def wilcox_test(x, y, alternative='two-sided'):
        x, y = x.dropna(), y.dropna()
        try:
            return mannwhitneyu(x, y, alternative=alternative)
        except ValueError:
            return None

    def yuen_test(x, y, alternative='two-sided', tr=0.1):
        x, y = x.dropna(), y.dropna()
        x_trimmed = trim_mean(x, proportiontocut=tr)
        y_trimmed = trim_mean(y, proportiontocut=tr)
        n_x, n_y = len(x), len(y)
        var_x = np.var(x, ddof=1)
        var_y = np.var(y, ddof=1)

        t_stat = (x_trimmed - y_trimmed) / np.sqrt((var_x / n_x) + (var_y / n_y))

        df = n_x + n_y - 2 * int(tr * (n_x + n_y))

        from scipy.stats import t
        p_value = t.sf(np.abs(t_stat), df) * 2
        if alternative == 'greater' and t_stat > 0:
            p_value /= 2
        elif alternative == 'less' and t_stat < 0:
            p_value /= 2

        return pd.Series({'statistic': t_stat, 'p_value': p_value})

    test_fun = {
        't-test': lambda x, y: err_t_test(x, y, alternative),
        'wilcox': lambda x, y: wilcox_test(x, y, alternative),
        'yuen': lambda x, y: yuen_test(x, y, alternative)
    }.get(test, None)

    if not test_fun:
        raise ValueError("Invalid test specified. Choose from 't-test', 'wilcox', or 'yuen'.")

    analysis = {}
    for term, data in calculation_spread.items():
        if term == "time_to_threshold":
            data = data.fillna(0)

        ct_sel = [col for col in data.columns if control in col]
        if not ct_sel:
            raise ValueError(f"Control '{control}' not found in columns.")

        stat_res = pd.DataFrame(index=data.columns, columns=["statistic", "p_value", "significant"])

        for col in data.columns:
            if col == control:
                test_result = test_fun(data[col], data[col])
            else:
                test_result = test_fun(data[col], data[ct_sel[0]])

            if test_result is not None:
                p_value = test_result['p_value'] if isinstance(test_result, pd.Series) else test_result.pvalue
                statistic = test_result['statistic'] if isinstance(test_result, pd.Series) else test_result.statistic
            else:
                p_value = np.nan
                statistic = np.nan

            stat_res.loc[col, "statistic"] = round(statistic, 2)
            stat_res.loc[col, "p_value"] = round(p_value, 5)

        stat_res["significant"] = ""
        for idx, pval in stat_res["p_value"].items():
            if not pd.isna(pval):
                if pval <= 0.0001:
                    stat_res.at[idx, "significant"] = '****'
                elif pval <= 0.001:
                    stat_res.at[idx, "significant"] = '***'
                elif pval <= 0.01:
                    stat_res.at[idx, "significant"] = '**'
                elif pval <= alpha:
                    stat_res.at[idx, "significant"] = '*'

        analysis[term] = stat_res.fillna("")

    return analysis