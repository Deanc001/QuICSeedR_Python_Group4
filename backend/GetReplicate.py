import pandas as pd
import numpy as np

def GetReplicate(plate):
    replicate_counts = {} #dictionary to keep track of counts for each sample
    #intialize empty data frame and fill with nan variables
    replicate_data= pd.DataFrame(np.nan, index=plate.index, columns=plate.columns)

    #iterate through plate data by row and column
    #loops through each cell in plate, updating replicate numbers in 'replicate data'
    #if sample id is found, then it counts and assigns replicate num if Nan then it leaves as is
    for col in plate.columns:
        for row in plate.index:
            sample_id = plate.loc[row,col]
            if pd.isna(sample_id): #if cell is empty, keep as Nan
                replicate_data.loc[row,col]= np.nan
            else:
                sample_id = str(sample_id) #convert sample ID to string to be consistent
                if sample_id not in replicate_counts:
                    replicate_counts[sample_id] =1 #initialize count if sample ID is new
                else:
                    replicate_counts[sample_id] +=1 #increments if sample ID is repeat
                
                #assign current replicate number to the replicate_data DataFrame
                replicate_data.loc[row,col]= replicate_counts[sample_id]

    return replicate_data



