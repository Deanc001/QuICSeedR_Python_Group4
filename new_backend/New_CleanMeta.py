import pandas as pd
import numpy as np


def clean_meta(raw, plate, replicate, split_content=False, split_by="_", split_into=None, del_na=True):
    #Type Checks
    if not isinstance(plate, pd.DataFrame) or not isinstance(replicate, pd.DataFrame):
        raise TypeError("plate and replicate must be pandas DataFrames.")
    if not isinstance(raw,pd.DataFrame):
        raise TypeError("raw must be a pandas DataFrame.")
    if not (split_content, bool):
        raise TypeError("split_content must be a boolean.")
    if not isinstance(split_by, str):
        raise TypeError("split_by must be a string.")
    if split_content and (not split_into or not all(isinstance(s, str) for s in split_into)):
        raise ValueError("If split_content is True, split_into must be a list of non-empty strings.")

    #Determine plate format based on num of columns in the panda data frame
    n_platecol = plate.shape[1]
    if n_platecol not in [13,25]:
        raise ValueError("Invalid plate column count. Expected 13 (96-well) or 25 (384-well).")
    plate_format = 96 if n_platecol ==13 else 384
    replicate = replicate.iloc[:,1:].values.flatten()

    #Make wells based on the plate format
    rows = [chr(i) for i in range(ord('A'), ord('H') + 1)] if plate_format == 96 else [chr(i) for i in range(ord('A'), ord('P') + 1)]
    cols = [f"{i:02}" for i in range(1, 13)] if plate_format == 96 else [f"{i:02}" for i in range(1, 25)]
    well = [f"{r}{c}" for r in rows for c in cols]

    #Flatten content data
    content = plate.iloc[:, 1:n_platecol].values.flatten()

    #Remove NaN if any
    if del_na:
        valid_indices = ~pd.isna(replicate)
        well = np.array(well)[valid_indices]
        content = content[valid_indices]
        replicate = replicate[valid_indices]

    #Combined content_replicate field
    content_replicate = [f"{c}_{r}" if pd.notna(c) and pd.notna(r) else None for c, r in zip(content, replicate)]

    #Meta DataFrame
    meta = pd.DataFrame({
        'well': well,
        'content': content,
        'replicate': replicate,
        'content_replicate': content_replicate,
        'format': plate_format
    })

    # Split content if requested
    if split_content:
        split_df = meta['content'].astype(str).str.split(split_by, expand=True)

        if split_df.shape[1] != len(split_into):
            raise ValueError(
                f"Number of split columns ({split_df.shape[1]}) does not match the length of 'split_into' ({len(split_into)}).")
        split_df.columns = split_into
        meta = pd.concat([meta, split_df], axis=1)

    return meta


