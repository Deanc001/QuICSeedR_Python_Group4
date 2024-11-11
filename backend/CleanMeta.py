import pandas as pd
import numpy as np
from GetReplicate import GetReplicate

def CleanMeta(raw, plate, replicate, split_content=False, split_by="_", split_into=None, del_na=True):
    if split_content and (split_into is None or len(split_into) == 0):
        raise ValueError("If split_content is True, split_into must be provided and cannot be empty.")
    
    n_platecol = 13 if plate.shape[1] == 13 else 25
    plate_format = 96 if n_platecol == 13 else 384
    
    replicate = replicate.iloc[:, 1:].values.flatten()
    
    def generate_wells(rows, cols):
        wells = [f"{r}{c}" for r in rows for c in cols]
        return wells
    
    if plate_format == 96:
        rows = list("ABCDEFGH")
        cols = [f"{i:02}" for i in range(1, 13)]
        n_row, n_col = 8, 12
    elif plate_format == 384:
        rows = list("ABCDEFGHIJKLMNOP")
        cols = [f"{i:02}" for i in range(1, 25)]
        n_row, n_col = 16, 24
    else:
        raise ValueError("Invalid format. Must be either 96 or 384.")
    
    well = generate_wells(rows, cols)
    
    content = plate.iloc[:, 1:n_platecol].values.flatten()
    
    if del_na:
        valid_well = ~pd.isna(replicate)
        well = np.array(well)[valid_well]
        content = content[valid_well]
        replicate = replicate[valid_well]
    
    vectorized_add = np.vectorize(lambda x, y: str(x) + "_" + str(int(y)))

    # Apply the function to both arrays
    content_replicate = vectorized_add(content, replicate)

    
    meta = pd.DataFrame({
        'well': well,
        'content': content,
        'replicate': replicate,
        'content_replicate': content_replicate,
        'format': plate_format
    })
    

    if split_content:
        split_df = meta['content'].str.split(split_by, expand=True)
    
        # Handle cases where split_df does not have enough columns by filling missing ones with NaN
        if split_df.shape[1] < len(split_into):
            for i in range(split_df.shape[1], len(split_into)):
                split_df[i] = np.nan

        if split_df.shape[1] != len(split_into):
            print("Content split resulted in columns:")
            print(split_df.head())
            raise ValueError(f"Number of split columns ({split_df.shape[1]}) does not match the length of 'split_into' ({len(split_into)}).")
        
        split_df.columns = split_into
        meta = pd.concat([meta, split_df], axis=1)
    
    return meta



if __name__ == "__main__":
    raw_96 = pd.read_excel('.././tutorials/data/20240716_s1_raw.xlsx')

    plate_96 = pd.read_excel('.././tutorials/data/20240716_s1_plate.xlsx')

    replicate_96 = GetReplicate(plate_96)

    meta_96 = CleanMeta(raw_96, plate_96, replicate_96)

    print(meta_96)