import pandas as pd
import numpy as np

def GetCalculation(raw, meta, norm=False, norm_ct=None, threshold_method= "stdv", time_skip= 5,sd_fold=3, bg_fold=3, rfu=5000, cycle_background=4, binw=6 ):

    #Check for valid threshold method, and check parameters
    if threshold_method not in ["stdv", "bg_ratio", "rfu_val"]:
        raise ValueError("Invalid threshold_method. Use 'stdv', 'bg_ratio, or 'rfu_val'.")
    if cycle_background > raw.shape[0]:
        raise ValueError("cycle_background exceeds number of rows in raw data")
    if norm and norm_ct is None:
        raise ValueError("norm_ct must be provided when norm is True")

    #Helper function to calc Maximum to Background Ratio (MPR)
    def calculate_mpr(raw, background):
        return raw.max(axis=0)/background #takes max value of each column in raw and divide by background

    #Helper function to determine threshold based on which method is chosen
    def calculate_threshold(nv, method, sd_fold, bg_fold, rfu):
        if method == "stdv":
            return np.mean(nv) + sd_fold*np.std(nv) #std deviation method
        elif method== "bg_ratio":
            return nv*bg_fold #Background ratio method
        else:
            return rfu #fixed RFU value

    #Helper func to calc time-to-threshold and rate of apprearance factor (RAF)
    # Finds when each sample crosses the threshold and calculates RAF by taking the inverse of the cross time
    def calculate_raf(raw, threshold, time_skip):
        time_to_threshold = []
        for column in raw.T:
            crossing_row= np.argmax(column[time_skip:] > threshold)
            if column[time_skip+crossing_row] <= threshold:
                time_to_threshold.append(np.nan)
            else:
                time_to_threshold.append(time_skip + crossing_row)
        raf=1/np.array(time_to_threshold, dtype=float)
        raf[np.isinf(raf)|np.isnan(raf)]=0
        return time_to_threshold, raf

    #Helper func to calc the Maximum Slope(MS) for each sample
    #Calculate Ms as the highest slope betwen points in each sample, using a window of size binw
    def calculate_ms(raw, binw):
        smoothed_slope = []
        for column in raw.T:
            slopes =[(column[i+binw]- column[i])/binw for i in range(len(column)-binw)]
            smoothed_slope.append(max(slopes, default=np.nan))
        return smoothed_slope

    #Background using specificed cycle_background row
    background= raw.iloc[cycle_background -1, :]
    nv =background.values
    threshold = calculate_threshold(nv, threshold_method, sd_fold, bg_fold, rfu)
    # calc mpr, raf, and ms
    mpr=calculate_mpr(raw, background)
    time_to_threshold, raf= calculate_raf(raw, threshold, time_skip)
    ms= calculate_ms(raw, binw)

    #combine results into dataframe
    calculation =pd.DataFrame({
        "time_to_threshold": time_to_threshold,
        "RAF":raf,
        "MPR":mpr,
        "MS":ms
    })

    #if normalization needed, this adjusts calculation using samples labeled as norm_ct in meta
    #normalize values if norm=true by dividing by the average for norm_ct-labeled samples in meta
    if norm:
        sel= meta[meta["content"]== norm_ct].index
        data_pos = calculation.loc[sel]
        terms =["time_to_threshold", "RAF", "MPR", "MS"]
        data_norm = pd.DataFrame(index=calculation.index, columns=terms)

        for term in terms:
            ave_term = data_pos[term].mean()
            data_norm[term]= calculation[term]/ave_term

        calculation =pd.concat([meta, data_norm], axis=1) #assigns normalized values
    else:
        calculation =pd.concat([meta, calculation], axis=1)

    calculation["XTH"]= np.where((calculation["time_to_threshold"]>0)& ~calculation["time_to_threshold"].isna(),1,0)

    return calculation


