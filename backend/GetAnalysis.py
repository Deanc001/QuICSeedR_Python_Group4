import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, wilcoxon
import warnings
import pingouin as pg #Yuen's Test package

def GetAnalysis(calculation_spread, control, test ='wilcox', alternative= 'two.sided', adjust_p = False, alpha=0.05):
    for i,df in enumerate(calculation_spread):          #Loops through dataframe and keeps track of index (i)
        if 'time_to_threshold' in df.columns:           #checks if time_to_threshold is in data frame columns
            df['time_to_threshold'].fillna(0, inplace=True)  #replaces na with 0 in data frame directly

    #err.test.t changed into err_test_t due to naming convention in python
    def err_test_t (x,y, **kwargs):  #kwargs is similar to ... in R, allows passing of additional params,
        x= x[~np.isnan(x)] #check if there is nan and then get rid of nan with ~ (not) symbol
        y= y[~np.isnan(y)]

        try:                                    #try t test on values, if t test succeed, result returned
            result =ttest_ind(x,y,**kwargs)
            return result
        except Exception as e:                  #if any error occurs, exception catches it and returns NA
            return None


    def yuen_test (x,y, tr=0.1, alternative ='two-sided'): #trim data is 10% which is default
        try:
            #Running Yuen's test using pinguion package
            result= pg.robust_ttest(x,y, tr=tr, alternative =alternative) #runs yuens on values
            statistic = result['T'].values[0]   #test statistic (T) from yuens test
            p_value = result['p-val'].values[0] #p-value from yuens test
            return {'statistic': statistic, 'p.value': p_value}
        except Exception as e:              #if theres an error, returns none,close to R which returns NA
            return None

    #Returns right stat test based on the test param
    def test_function_check(test, alternative):
        if test == 't-test':            #uses ttest_ind from scipy
            def test_fun(x,y):
                try:
                    return ttest_ind(x,y, alternative = alternative)
                except Exception as e:
                    return None
        elif test == 'wilcox':          #uses wilcoxon from scipy
            def test_fun(x,y):
                try:
                    return wilcoxon(x,y, alternative = alternative)
                except Exception as e:
                    return None
        elif test == 'yuen':            #calls yuen from previous yuen function
            def test_fun(x,y):
                return yuen_test(x,y, alternative = alternative)
        else:
            raise ValueError("Invalid Test Specified")          #if invalid test, then returns value error
        return test_fun

    #test function based on user choice
    test_fun = test_function_check(test, alternative)

    analysis= []

    #stat_res creates empty data frame to store result of stat tests, control_col finds control column
    for df in calculation_spread:
        stat_res =pd.DataFrame(columns=["statistic", "p_value", "adj_p", "significant"], index=df.columns)
        control_col = df.filter(regex=control).columns[0]


        for col in df.columns:    #loops over each column (col) in the data frame
            try:
                t_res = test_fun(df[col].dropna(), df[control_col].dropna()) #call test fun for column and ctrl column
                if t_res is None:
                    continue

                if isinstance(t_res, dict):   #For Yuen's test (dictionary), extracts p_val and stats
                    p_value =t_res['p.value']
                    statistic = t_res['statistic']
                else:
                    p_value =t_res.pvalue           #extracts values directly from result obj
                    statistic =t_res.statistic

                stat_res.loc[col, "statistic"] = round(statistic, 2) if statistic is not None else None
                stat_res.loc[col, "p_value"]= round(p_value, 5)   #extracted values are rounded and stored in stat_res

            except Exception:
                stat_res.loc[col, "p_value"] = np.nan


        # if adjust_p true then uses Benjamini-Hochberg method which adjusts the p_val col and stored in adj_p and if false, original p-vals copied to adJ_p col
        if adjust_p:
            p_adj = pd.Series(stat_res["p_value"]).transform(lambda p: pg.multicomp(p.values, method='fdr_bh')[1])
            stat_res["adj_p"] = p_adj.round(5)
        else:
            stat_res["adj_p"] = stat_res["p_value"]

        #assigns stars based on the adjusted p-vals based on the certain thresholds
        stat_res["significant"] = stat_res["adj_p"].apply(
            lambda p: '****' if p<= 0.0001 else (
                '***' if p<= 0.001 else(
                    '**' if p <=0.01 else (
                        '*' if p<= alpha else ''
                    )
                )
            )
        )

        analysis.append(stat_res)

    return analysis





