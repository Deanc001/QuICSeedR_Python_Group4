import pandas as pd
import numpy as np


def clean_raw(meta, raw, plate_time, cycle_total=None):
    #Set the default total number of cycles (timepoints)
    if cycle_total is None or len(str(cycle_total)) == 0:
        cycle_total = raw.shape[0] - 1  #Skip the header row

    #Remove the first row (header) and first two columns (non-data columns)
    raw = raw.iloc[1:, 2:]

    #keep only columns that match the wells listed in the metadata
    #convert values to numeric, coerce errors to NaN
    raw = raw.loc[:cycle_total, meta['well']].apply(pd.to_numeric, errors='coerce')

    #Flatten into a 1D array, then reshape back into (timepoints x samples) shape
    raw = raw.values.flatten()
    raw = np.reshape(raw, (cycle_total, -1))

    #Extract time values for the index (row names)
    row_names = plate_time.iloc[:cycle_total, 0].values.flatten()

    #Extract sample-replicate names for the columns
    col_names = meta['content_replicate'].values

    #Build the final cleaned DataFrame with time as rows and samples as columns
    raw_df = pd.DataFrame(raw, index=row_names, columns=col_names)

    return raw_df