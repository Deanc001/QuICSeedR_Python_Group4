import pandas as pd
import os
from GetReplicate import get_replicate

"""
Reads multiple experimental datasets from subfolders.
Each folder should contain:
    -A plate layout file (plate_subfix)
    -A raw fluorescence file(raw_subfix)

Parameters:
    path(str): Path to the root folder containing experiment subfolders
    plate_subfix(str): Identifier for the plate layout file
    raw_subfix(str): Identifier for the raw fluorescence data 
    helper_func (function,optional): Function to apply extra formatting to plate data
    
Returns: 
    dict: A dictionary where each key is an experiment name (folder), 
    and each value is a dict with plate, raw, and replicate data
"""

def BulkReadMARS(path, plate_subfix, raw_subfix, helper_func=None):

    #Get list of all subdirectories in the given path (each should be experiment)
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    
    mylist = {} #Output dictionary
    
    for folder in folders:
        folder_path = os.path.join(path, folder) #Full path to the experiment folder

        #Find all Excel files in the folder
        files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

        #Seperate the plate layout and raw data files based on name patterns
        plate_files = [f for f in files if plate_subfix in f]
        raw_files = [f for f in files if raw_subfix in f]

        #Skip this folder if either required file is missing
        if not plate_files or not raw_files:
            print(f"Skipping folder '{folder}' due to missing files.")
            continue

        #Get full paths to the plate and raw files
        plate_path = os.path.join(folder_path, plate_files[0])
        raw_path = os.path.join(folder_path, raw_files[0])
        
        #Load both excel files into pandas DataFrames
        plate_data = pd.read_excel(plate_path)
        raw_data = pd.read_excel(raw_path)


        #Extract replicate groupings from plate layout using helper function
        replicate_data = get_replicate(plate_data) 

        #Optional: apply custom formatting function to plate layout (if provided)
        if helper_func:
            plate_data = plate_data.apply(helper_func)


        #Store everything in the final dictionary under the experiment name
        mylist[folder] = {
            'plate': plate_data,
            'raw': raw_data,
            'replicate': replicate_data
        }
    
    return mylist


#Sample use-case when running this file directly
if __name__ == "__main__":
    grinder_data = BulkReadMARS(
        path = '.././tutorials/data/grinder/',
        plate_subfix = 'plate',
        raw_subfix = 'raw')

    print(grinder_data)