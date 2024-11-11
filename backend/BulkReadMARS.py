import pandas as pd
import os
from GetReplicate import GetReplicate

def BulkReadMARS(path, plate_subfix, raw_subfix, helper_func=None):

    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    
    mylist = {}
    
    for folder in folders:
        folder_path = os.path.join(path, folder)
        
        files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
        
        plate_files = [f for f in files if plate_subfix in f]
        raw_files = [f for f in files if raw_subfix in f]
        
        plate_path = os.path.join(folder_path, plate_files[0])
        raw_path = os.path.join(folder_path, raw_files[0])

        if(len(plate_path) == 0 or len(raw_path) == 0):
            print("Skipping folder due to missing files")
            continue
        
        plate_data = pd.read_excel(plate_path)
        raw_data = pd.read_excel(raw_path)
        replicate_data = GetReplicate(plate_data) 
        
        if helper_func:
            plate_data = plate_data.apply(helper_func)
        
        mylist[folder] = {
            'plate': plate_data,
            'raw': raw_data,
            'replicate': replicate_data
        }
    
    return mylist


if __name__ == "__main__":
    grinder_data = BulkReadMARS(path = '.././tutorials/data/grinder/', plate_subfix = 'plate', raw_subfix = 'raw')

    print(grinder_data)