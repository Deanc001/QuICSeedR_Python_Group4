import pandas as pd
import numpy as np


def clean_meta(raw, plate, replicate, split_content=False, split_by="_", split_into=None, del_na=True):
    #Type Checks
    if not isinstance(plate, pd.DataFrame):
        raise TypeError("Expected 'plate' to be a pandas DataFrame.")
    if not isinstance:
        raise TypeError("Expected 'replicate' to be a pandas DataFrame")
    if not isinstance:
        raise TypeError("Expected 'split-content' to be a boolean.")

    #Empty DataFrame
    if plate.empty:
        raise ValueError("The 'plate' DataFrame is empty.")
    if replicate.empty:
        raise ValueError("The 'replicate' DataFrame is empty.")

    #Shape Compatibility Check
    if plate.shape[0] != replicate.shpae[0]:
        raise ValueError("The 'plate' and 'replicate' DataFrames must have same number of rows")

    #Determine plate format
    plate_format =96 if plate.shape[1] == 13 else 384
    replicate_values =replicate.iloc[:,1:].to_numpy().flatten()

    #Flatten content vals
    content_values = plate.iloc[:,1:plate.shape[1]].to_numpy().flatten()

    #Nan removal
    if del_na:
        valid_mask = ~pd.isna(replicate_values)
        content_values = content_values[valid_mask]
        replicate_values= replicate_values[valid_mask]

    #Generate `content_replicate` column
    content_replicate_values = np.where(pd.notna(content_values) & pd.notna(replicate_values), content_values + "_" + replicate_values, None)

    # Create DataFrame
    meta = pd.DataFrame({
        'content': content_values,
        'replicate': replicate_values,
        'content_replicate': content_replicate_values,
        'format': plate_format
    })

    # Split content if needed
    if split_content:
        split_df = meta['content'].str.split(split_by, expand=True)
        if split_df.shape[1] != len(split_into):
            raise ValueError(
                f"Number of split columns ({split_df.shape[1]}) does not match the length of 'split_into' ({len(split_into)})."
            )
        split_df.columns = split_into
        meta = pd.concat([meta, split_df], axis=1)

    return meta
