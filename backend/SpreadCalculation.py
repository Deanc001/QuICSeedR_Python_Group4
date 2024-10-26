import pandas as pd

def SpreadCalculation(calculation, id_col="content", rep_col="replicate", terms=['RAF', 'MPR', 'MS']):
    
    if not all(col in calculation.columns for col in [id_col, rep_col]):
        raise ValueError("id_col and rep_col must be present in the calculation data frame")
    
    if terms is None:
        terms = ['time_to_threshold', 'RAF', 'MPR', 'MS']
        
    if not all(term in calculation.columns for term in terms):
        raise ValueError("Not all specified terms are present in the calculation data frame")
    
    def spread_term(data, term):
        
        spread_df = data.pivot(index=rep_col, columns=id_col, values=term).reset_index(drop=True)
        return spread_df
    
    calculation_spread = {term: spread_term(calculation, term) for term in terms}
    
    return calculation_spread