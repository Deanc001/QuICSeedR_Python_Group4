import pandas as pd
import numpy as np

def SummarizeResult(analysis = None, calculation = None, sig_method="xth_percent", method_threshold=5):
    
    if not isinstance(calculation, pd.DataFrame) or 'content' not in calculation.columns:
        raise ValueError("'calculation' must be a DataFrame with a 'content' column")
    
    unique_content = calculation['content'].unique()
    result = pd.DataFrame({
        'content': unique_content,
        'result': [''] * len(unique_content),
        'method': [sig_method] * len(unique_content)
    })
    
    sub = calculation.iloc[:, :3]
    sub_reshaped = sub.pivot(index='content', columns='replicate')
    
    position = (calculation
                .filter(like='well.')
                .melt(id_vars=['content'], value_name='well_value')
                .dropna(subset=['well_value'])
                .groupby('content')
                .agg(wells=('well_value', lambda x: '-'.join(sorted(x.astype(str)))))
                .reset_index())
    
    result['position'] = result['content'].map(position.set_index('content')['wells'])
    
    if analysis is not None and isinstance(analysis, dict):
        valid_sig_methods = ['metric_count', 'xth_count', 'xth_percent'] + list(analysis.keys())
        if sig_method not in valid_sig_methods:
            raise ValueError(f"Invalid sig_method. Must be one of: {', '.join(valid_sig_methods)}")
        
        for stat_name, stat in analysis.items():
            if 'significant' not in stat.columns or 'p_value' not in stat.columns:
                print(f"Skipping {stat_name} due to missing 'significant' or 'p_value' column")
                continue
            
            content_col = stat['content'] if 'content' in stat.columns else stat.index
            result[f"{stat_name}_sig"] = stat['significant'].reindex(result['content'], fill_value='')
            result[f"{stat_name}_p"] = stat.get('adj_p', stat['p_value']).reindex(result['content'], fill_value=np.nan)
            
        sig_columns = result.filter(like='_sig').columns
        result['metric_count'] = result[sig_columns].apply(lambda x: x.str.contains('*').sum(), axis=1)
        
        if sig_method == 'metric_count':
            result['result'] = np.where(result['metric_count'] >= method_threshold, '*', '')
        elif sig_method in analysis:
            sig_column = f'{sig_method}_sig'
            if sig_column in result.columns:
                result['result'] = np.where(result[sig_column].str.contains('*'), '*', '')
            else:
                print(f"Column {sig_column} not found in results. No overall result calculated.")
                
    else:
        print("'analysis' is empty or not a dictionary. Metric, metric count, and p-value columns will not be included.")
                
                
    xth_count = calculation.groupby('content')['XTH'].sum().reset_index()
    result['xth_count'] = result['content'].map(xth_count.set_index('content')['XTH'])
        
    total_rep = (calculation.groupby('content')['replicate'].max().reset_index().rename(columns={'replicate': 'total_rep'}))
    result['total_rep'] = result['content'].map(total_rep.set_index('content')['total_rep'])
        
    result['xth_percent'] = (result['xth_count'] / result['total_rep'] * 100).round(2)
        
    if sig_method == 'xth_count':
        result['result'] = np.where(result['xth_count'] >= method_threshold, '*', '')
    elif sig_method == 'xth_percent':
        result['result'] = np.where(result['xth_percent'] >= method_threshold, '*', '')
            
    return result