import pandas as pd


def summarize_result(analysis=None, calculation=None, sig_method="xth_percent", method_threshold=50):
    if calculation is None or 'content' not in calculation.columns:
        raise ValueError("'calculation' must be a DataFrame with a 'content' column.")

    calculation['content'] = calculation['content'].astype(str)
    unique_content = calculation['content'].unique()
    result = pd.DataFrame({'content': unique_content, 'result': "", 'method': sig_method})

    sub = calculation[['content', 'replicate', 'well']].copy()
    sub_wide = sub.pivot(index='content', columns='replicate', values='well').reset_index()
    sub_long = pd.melt(sub_wide, id_vars=['content'], var_name='well_column', value_name='well_value')
    position = (sub_long.dropna()
                .groupby('content')['well_value']
                .apply(lambda x: '-'.join(sorted(map(str, x))))
                .reset_index(name='wells'))
    result = result.merge(position, on='content', how='left')

    result['content'] = result['content'].astype(str)

    if analysis and isinstance(analysis, dict) and len(analysis) > 0:
        valid_sig_methods = ["metric_count", "xth_count", "xth_percent"] + list(analysis.keys())
        if sig_method not in valid_sig_methods:
            raise ValueError(f"Invalid sig_method. Must be one of: {', '.join(valid_sig_methods)}")

        for stat_name, stat in analysis.items():
            if 'content' not in stat.columns:
                stat = stat.reset_index()
            stat['content'] = stat['content'].astype(str)

            if not all(col in stat.columns for col in ["significant", "p_value"]):
                print(f"Warning: Skipping {stat_name} due to missing 'significant' or 'p_value' column.")
                continue

            cols_to_merge = ['content', 'significant', 'p_value']
            if 'adj_p' in stat.columns:
                cols_to_merge.append('adj_p')

            stat = stat[cols_to_merge].rename(columns={
                'significant': f"{stat_name}_sig",
                'p_value': f"{stat_name}_p",
                'adj_p': f"{stat_name}_p"
            })

            result = result.merge(stat, on='content', how='left', indicator=True)
            result = result.drop(columns=['_merge'])

        sig_columns = [col for col in result.columns if col.endswith('_sig')]
        result['metric_count'] = result[sig_columns].apply(lambda row: sum('*' in str(val) for val in row), axis=1)

        if sig_method == "metric_count":
            result.loc[result['metric_count'] >= method_threshold, 'result'] = "*"
        elif sig_method in ["MS", "MPR", "RAF"]:
            sig_column = f"{sig_method}_sig"
            if sig_column in result.columns:
                result.loc[result[sig_column].str.contains(r'\*', na=False), 'result'] = "*"
            else:
                print(f"Warning: Column {sig_column} not found in results. No overall result calculated.")
    elif analysis is not None:
        print("Warning: 'analysis' is empty or not a dictionary."
              "Metric, metric count, and metric p-value columns will not be included.")

    xth_count = calculation.groupby('content')['XTH'].sum().reset_index(name='xth_count')
    result = result.merge(xth_count, on='content', how='left')

    total_rep = calculation.groupby('content')['replicate'].max().reset_index(name='total_rep')
    result = result.merge(total_rep, on='content', how='left')

    result['xth_percent'] = round((result['xth_count'] / result['total_rep']) * 100, 2)

    if sig_method == "xth_count":
        result.loc[result['xth_count'] >= method_threshold, 'result'] = "*"
    elif sig_method == "xth_percent":
        result.loc[result['xth_percent'] >= method_threshold, 'result'] = "*"

    return result