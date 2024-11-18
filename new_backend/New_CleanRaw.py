import pandas as pd
import numpy as np

def clean_raw(meta, plate_time, cycle_total = None):
    #check input types
    if not isinstance(metadata, pd.DataFrame):
        raise TypeError("metadata must be a pandas DataFrame.")
    if not isinstance(raw_data, pd.DataFrame):
        raise TypeError("raw_data must be a pandas DataFrame.")
    if not isInstance(plate_times, pd.DataFrame):
        raise TypeError("plate_times must be a pandas DataFrame.")


    #Check for 'well' and 'content replicate' in metadata
    if 'well' not in metadata.columns:
        raise KeyError("'metadata' must contain a 'well' column.")
    if 'content_replicate' not in metadata.columns:
        raise KeyError("'content_replicate' must contain a 'content_replicate' column")

    #Cycle total default case
    if cycle_total is None or not isinstance(cycle_total, int):
        cycle_total= raw_data.shape[0]-1

    #Select and clean raw data, ignores first row and first two columns
    cleaned_raw = raw.data.iloc[1:,2:]
    cleaned_raw = cleaned_raw.loc[:cycle_total, metadata['well']].apply(pd.to_numeric, errors='coerce')
    cleaned_raw = cleaned_raw.values.flatten()
    reshaped_raw = np.reshape(cleaned_raw, (cycle_total, -1))

    #Row and Column names
    row_labels = plate_time.iloc[:cycle_total, 0].values.flatten()
    column_labels = metadata['content_replicate'].values


    #Cleaned the DataFrame
    raw_df = pd.DataFrame(reshaped_raw, index=row_labels, column= column_labels)

    return raw_df






