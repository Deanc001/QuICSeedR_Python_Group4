import pandas as pd
import re

def ConvertTime(raw):
    #Take out time column and convert to dataframe  (change)
    time = pd.DataFrame({'time':raw.iloc[1:,1].copy()})
    time['time'] =time['time'].astype(str)  #make sure values are strings

    # Find and convert 'hours' and 'minutes' to decimal hours  (change)
    time['hours'] = time['time'].str.extract(r'(\d+)\s*h', expand=False).astype(float).fillna(0)
    time['minutes'] = time['time'].str.extract(r'(\d+)\s*min', expand=False).astype(float).fillna(0)

    # Convert to decimal hours (change)
    time['decimal_hours'] = time['hours'] + (time['minutes'] / 60)

    # Use decimal hours if conversion is present, otherwise fall back to numeric conversion (change)
    time['time_converted'] = time['decimal_hours'].where(time['hours'] + time['minutes'] > 0,
                                                         pd.to_numeric(time['time'], errors='coerce'))

    return time[['time', 'time_converted']]


if __name__ == "__main__":
    try:
        raw_96 = pd.read_excel('.././tutorials/data/20240716_s1_raw.xlsx')
        plate_time_96 = ConvertTime(raw_96)
        print(plate_time_96)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
