import pandas as pd
import numpy as np


def clean_meta(raw, plate, replicate, split_content=False, split_by="_", split_into=None, del_na=True):
    if split_content and (not split_into or len(split_into) == 0):
        raise ValueError("If split_content is True, split_into must be provided and cannot be empty.")


    #Determine if plate is 96-well (13 columns) or 384-well (25 columns)
    n_platecol = 13 if plate.shape[1] == 13 else 25
    plate_format = 96 if n_platecol == 13 else 384

    #Flatten the replicate matrix, ignoring first column (likely well labels)
    replicate = replicate.iloc[:, 1:].values.flatten()

    #Helper function to generate well names (eg A01, B12)
    def generate_wells(rows, cols):
        return [f"{r}{c}" for r in rows for c in cols]

    #Choose rows and column based on plate format
    if plate_format == 96:
        rows = [chr(i) for i in range(ord('A'), ord('H') + 1)]
        cols = [f"{i:02}" for i in range(1, 13)]
    elif plate_format == 384:
        rows = [chr(i) for i in range(ord('A'), ord('P') + 1)]
        cols = [f"{i:02}" for i in range(1, 25)]
    else:
        raise ValueError("Invalid format. Must be either 96 or 384.")
    well = generate_wells(rows, cols)   #Generate full list of well names

    #Flatten plate content (ignoring first column)
    content = plate.iloc[:, 1:n_platecol].values.flatten()

    #Optionally remove wells with missing replicate info
    if del_na:
        valid_indices = ~pd.isna(replicate)
        well = np.array(well)[valid_indices]
        content = content[valid_indices]
        replicate = replicate[valid_indices]

    #Combine sample ID and replicate number into one column
    content_replicate = [f"{c}_{r}" if not pd.isna(c) and not pd.isna(r) else None for c, r in zip(content, replicate)]

    #Construct main metadata DataFrame
    meta = pd.DataFrame({
        'well': well,
        'content': content,
        'replicate': replicate,
        'content_replicate': content_replicate,
        'format': plate_format
    })

    #Split sample ID into multiple columns
    if split_content:
        split_df = meta['content'].str.split(split_by, expand=True)

        if split_df.shape[1] != len(split_into):
            raise ValueError(
                f"Number of split columns ({split_df.shape[1]}) does not match the length of 'split_into' ({len(split_into)}).")
        split_df.columns = split_into

        meta = pd.concat([meta, split_df], axis=1) #Add new columns to the metadata

    return meta