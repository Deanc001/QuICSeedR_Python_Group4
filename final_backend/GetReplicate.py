import pandas as pd
import numpy as np


def get_replicate(plate):
    replicate_counts = {} #Dictionary to count how many times each sample has appeared
    replicate_data = pd.DataFrame(np.nan, index=plate.index, columns=plate.columns) #Output Dataframe with same shape as input
    
    for col in plate.columns: #Loop through each column (well column)
        for row in plate.index: #Loop through each row (well row)
            sample_id = plate.at[row, col] #Get the sample ID at the current well
            if pd.isna(sample_id):  #If the well is empty (NaN), skip it
                replicate_data.at[row, col] = np.nan
            else:
                sample_id = str(sample_id) #Convert sample ID to string (ensures consistent keys)
                if sample_id not in replicate_counts: #If this is the first time we've seen this sample
                    replicate_counts[sample_id] = 1
                else:
                    replicate_counts[sample_id] += 1 #Otherwise increment the count
                replicate_data.at[row, col] = replicate_counts[sample_id] #Assign the current replicate number

    return replicate_data