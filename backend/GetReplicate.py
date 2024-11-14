import pandas as pd
import numpy as np

def GetReplicate(plate):
    replicate_counts = {} #dictionary to keep track of counts for each sample
    
    #intialize empty data frame for storing replicate counts
    replicate_data= pd.DataFrame(index=plate.index, columns=plate.columns)

   #Iterate over DataFrame Values to populate replicate counts
    for col in plate.columns:
        for row in plate.index:
            sample_id = plate.at[row,col]  #Changed loc into at since only one value is accessed in data frame
            if pd.isna(sample_id): #if cell is empty, keep as Nan
                replicate_data.at[row,col]= np.nan  
            else:
                #start/increment the count for the sample_id
                replicate_counts[sample_id] = replicate_counts.get(sample_id, 0) +1
                replicate_data.at[row,col] = replicate_counts[sample_id] #assign the count

    return replicate_data



