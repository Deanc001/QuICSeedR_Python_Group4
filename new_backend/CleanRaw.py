import pandas as pd
import numpy as np


def clean_raw(meta, raw, plate_time, cycle_total=None):
    if cycle_total is None or len(str(cycle_total)) == 0:
        cycle_total = raw.shape[0] - 1

    raw = raw.iloc[1:, 2:]
    raw = raw.loc[:cycle_total, meta['well']].apply(pd.to_numeric, errors='coerce')
    raw = raw.values.flatten()
    raw = np.reshape(raw, (cycle_total, -1))

    row_names = plate_time.iloc[:cycle_total, 0].values.flatten()
    col_names = meta['content_replicate'].values

    raw_df = pd.DataFrame(raw, index=row_names, columns=col_names)

    return raw_df
