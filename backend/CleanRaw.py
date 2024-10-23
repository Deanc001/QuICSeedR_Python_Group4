import pandas as pd
import numpy as np
from ConvertTime import ConvertTime
from GetReplicate import GetReplicate
from CleanMeta import CleanMeta

def CleanRaw(meta, raw, plate_time, cycle_total=None):

    if cycle_total is None or cycle_total == 0:
        cycle_total = raw.shape[0] - 1

    raw = raw.iloc[1:, 2:]

    raw = raw.iloc[:cycle_total].loc[:, meta['well']]

    raw = np.array(raw).flatten().astype(float)
    raw = raw.reshape(cycle_total, -1)

    row_names = plate_time.iloc[:cycle_total, 0].values
    raw = pd.DataFrame(raw, index=row_names, columns=meta['content_replicate'])

    return raw


raw_96 = pd.read_excel('.././tutorials/data/20240716_s1_raw.xlsx')

plate_96 = pd.read_excel('.././tutorials/data/20240716_s1_plate.xlsx')

plate_time_96 = ConvertTime(raw_96)

replicate_96 = GetReplicate(plate_96)

meta_96 = CleanMeta(raw_96, plate_96, replicate_96)

cleanraw_96 = CleanRaw(meta_96, raw_96, plate_time_96)

print(cleanraw_96)

