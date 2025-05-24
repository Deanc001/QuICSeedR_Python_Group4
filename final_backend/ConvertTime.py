import pandas as pd


def convert_time(raw):
    #Extract the time column (2nd column), skipping the first row (header)
    time = raw.iloc[1:, 1].copy()
    time = pd.DataFrame({'time': time}) #Convert to DataFrame
    time['time'] = time['time'].astype(str) #Ensure string type for regex operations

    #If time strings contain "min", extract hours and minutes separately
    if time['time'].str.contains('min', na=False).any():
        hours = time['time'].str.extract(r'(\d+)\s*h')[0].astype(float).fillna(0)
        minutes = time['time'].str.extract(r'(\d+)\s*min')[0].fillna(0).astype(float)

        #Convert to decimal hours: eg, 2h 30 min -> 2.5
        decimal_hours = hours + (minutes / 60)
        time['time'] = decimal_hours
    else:

        #If not in "min" format, just try converting to numbers directly
        time['time'] = pd.to_numeric(time['time'], errors='coerce')

    return time #Return standardized time Dataframe