import pandas as pd
import numpy as np


def get_replicate(plate):
    replicate_counts = {}
    replicate_data = pd.DataFrame(np.nan, index=plate.index, columns=plate.columns)
    
    for col in plate.columns:
        for row in plate.index:
            sample_id = plate.at[row, col]
            if pd.isna(sample_id):
                replicate_data.at[row, col] = np.nan
            else:
                sample_id = str(sample_id)
                if sample_id not in replicate_counts:
                    replicate_counts[sample_id] = 1
                else:
                    replicate_counts[sample_id] += 1
                replicate_data.at[row, col] = replicate_counts[sample_id]
    return replicate_data
