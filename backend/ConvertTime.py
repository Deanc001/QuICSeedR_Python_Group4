import pandas as pd
import re

def ConvertTime(raw):

    time = raw.iloc[1:, 1].copy()

    time = pd.DataFrame({'time': time})

    time['time'] = time['time'].astype(str)
    
    if time['time'].str.contains('min', na=False).any():

        hours = time['time'].str.extract(r'(\d+)\s*h')[0].astype(float).fillna(0)
        minutes = time['time'].str.extract(r'(\d+)\s*min')[0].fillna(0).astype(float)

        decimal_hours = hours + (minutes / 60)
        time['time'] = decimal_hours
    else:
        time['time'] = pd.to_numeric(time['time'], errors='coerce')

    return time


raw_96 = pd.read_excel('.././tutorials/data/20240716_s1_raw.xlsx')

plate_time_96 = ConvertTime(raw_96)

print(plate_time_96)