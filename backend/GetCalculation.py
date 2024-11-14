import pandas as pd
import numpy as np


def GetCalculation(raw, meta, norm=False, norm_ct=None, threshold_method="stdv", time_skip=5,
                    sd_fold=3, bg_fold=3, rfu=5000, cycle_background=4, binw=6):
    
    #Set Display Precision
    pd.set_option("display.precision", 9)

    if threshold_method not in ["stdv", "bg_ratio", "rfu_val"]:
        raise ValueError("Invalid threshold_method. Use 'stdv', 'bg_ratio', or 'rfu_val'.")
    if cycle_background > raw.shape[0]:
        raise ValueError("cycle_background exceeds number of rows in raw data.")
    if norm and norm_ct is None:
        raise ValueError("norm_ct must be provided when norm is True.")
    
    #Function to calculate Maximum Production Rate (MPR)
    def calculate_mpr(raw, background):
        return raw.max(axis=0) / background

    #Function to calculate threshold based on specified method
    def calculate_threshold(nv, method, sd_fold, bg_fold, rfu):
        if method == "stdv":
            variance = np.sum((nv - np.mean(nv)) ** 2) / (len(nv) - 1)
            std_dev = np.sqrt(variance)
            return np.mean(nv) + sd_fold * std_dev
        elif method == "bg_ratio":
            return nv * bg_fold
        else:
            return rfu

    def calculate_raf(raw, threshold, time_skip):
        time_to_threshold = []
        for column in raw.columns:
            crossing_rows = np.where(raw[column].values[time_skip:] > threshold)[0]
            if len(crossing_rows) == 0:
                time_to_threshold.append(np.nan)
            else:
                test = float(raw.index[crossing_rows[0] + time_skip])
                time_to_threshold.append(test)
        raf = 1 / np.array(time_to_threshold, dtype=float)
        raf[np.isinf(raf) | np.isnan(raf)] = 0
        return time_to_threshold, raf

    def calculate_ms(raw, binw):
        n = raw.shape[0]
        smoothed_slope = pd.DataFrame({
            col: [(raw[col].iloc[i + binw] - raw[col].iloc[i]) / binw
                  for i in range(n - binw)]
            for col in raw.columns
        })
        return smoothed_slope.max(axis=0, skipna=True).values

    background = raw.iloc[cycle_background-1, :].astype(float)
    nv = background.values
    threshold = calculate_threshold(nv, threshold_method, sd_fold, bg_fold, rfu)
    mpr = calculate_mpr(raw, background)
    time_to_threshold, raf = calculate_raf(raw, threshold, time_skip)
    ms = calculate_ms(raw, binw)

    calculation = pd.DataFrame({
        'time_to_threshold': time_to_threshold,
        'RAF': raf,
        'MPR': mpr,
        'MS': ms
    }, index=raw.columns)

    if norm:
        matching_meta = meta[meta['content'] == norm_ct]
        matching_replicates = matching_meta['content_replicate']
        sel = calculation.index.intersection(matching_replicates)

        if sel.empty:
            raise ValueError("No matching entries found for norm_ct in calculation index.")

        data_pos = calculation.loc[sel, :]
        terms = ["time_to_threshold", "RAF", "MPR", "MS"]
        data_norm = pd.DataFrame({
            term: calculation[term] / data_pos[term].mean() for term in terms
        }, index=calculation.index)
        calculation = pd.concat([meta.reset_index(drop=True), data_norm.reset_index(drop=True)], axis=1)
    else:
        calculation = pd.concat([meta.reset_index(drop=True), calculation.reset_index(drop=True)], axis=1)

    calculation['XTH'] = np.where((calculation['time_to_threshold'].notna()) &
                                  (calculation['time_to_threshold'] > 0), 1, 0)

    return calculation
