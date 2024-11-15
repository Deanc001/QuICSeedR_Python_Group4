def spread_calculation(calculation, id_col="content", rep_col="replicate", terms=None):
    if id_col not in calculation.columns or rep_col not in calculation.columns:
        raise ValueError("id_col and rep_col must be present in the calculation DataFrame.")
    if terms is None:
        terms = ['time_to_threshold', 'RAF', 'MPR', 'MS']
    if not all(term in calculation.columns for term in terms):
        raise ValueError("Not all specified terms are present in the calculation DataFrame.")

    def spread_term(data, term):
        pivoted = data[[id_col, rep_col, term]].pivot(index=rep_col, columns=id_col, values=term)
        return pivoted.reset_index(drop=True)

    calculation_spread = {term: spread_term(calculation, term) for term in terms}

    return calculation_spread
