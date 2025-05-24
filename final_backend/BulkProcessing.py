from ConvertTime import ConvertTime
from BulkReadMARS import BulkReadMARS
from CleanMeta import CleanMeta
from CleanRaw import CleanRaw

"""
Runs the full analysis pipeline on multiple FSAA datasets (eg from BulkReadMars)

Parameters:
    data(dict): Output from BulkReadMARS, each key is a plate/experiment
    do_analysis (bool): Whether to perform statistical analysis
    params (dict): Optional parameters for each processing step. 
    verbose (bool): If true, print progress and errors for debugging
    
Returns:
    dict: Combined cleaned raw data, calculations, and summarized results. 
"""

def BulkProcessing(data, do_analysis=True, params=None, verbose=False):

    if params is None:
        params = {}

    #Initialize output containers
    subcalculation = {}
    subcleanraw = {}
    subresult = {}

    #Logging utility
    def log(*args):
        if verbose:
            print(*args)
    
    # Process each experiment/plate one by one
    for j, experiment in enumerate(data):
        plate = data[experiment]['plate']
        raw = data[experiment]['raw']
        replicate = data[experiment]['replicate']
        
        log(f"Processing plate {j + 1}")
        log(f"Dimensions of raw: {raw.shape}")

        #Step 1: Convert time axis
        plate_time = ConvertTime(raw, **(params.get('ConvertTime', {})))

        #Step 2: Clean and structure metadata
        meta = CleanMeta(raw=raw, plate=plate, replicate=replicate, **(params.get('CleanMeta', {})))

        #Step 3: Clean the fluorescence data
        clean_raw_params = params.get('CleanRaw', {})

        # Clean raw
        try:
            raw = CleanRaw(meta=meta, raw=raw, plate_time=plate_time, **clean_raw_params)
        except Exception as e:
            log(f"Error in CleanRaw for plate {j + 1}: {str(e)}")
            continue
        
        if raw is None:
            log(f"Skipping further processing for plate {j + 1}")
            continue
        
        log(f"Dimensions of cleaned raw: {raw.shape}")
        
        #Step 4: Calculate biological metrics (eg RAF, MPR, etc.)
        try:
            calculation = GetCalculation(raw=raw, meta=meta, **(params.get('GetCalculation', {})))
        except Exception as e:
            log(f"Error in GetCalculation for plate {j + 1}: {str(e)}")
            continue
        
        if calculation is None:
            log(f"Skipping further processing for plate {j + 1}")
            continue
        
        #Step 5: Statistical analysis (eg Wilcoxon test)
        if do_analysis:
            calculation_spread = SpreadCalculation(calculation, **(params.get('SpreadCalculation', {})))
            analysis = GetAnalysis(calculation_spread, **(params.get('GetAnalysis', {})))
        
        #Step 6: Summarize results for export
        try:
            result = SummarizeResult(
                analysis=analysis if do_analysis else None, 
                calculation=calculation, 
                **(params.get('SummarizeResult', {}))
            )
        except Exception as e:
            log(f"Error in SummarizeResult for plate {j + 1}: {str(e)}")
            return None

        #Save successful outputs
        if result is not None:
            subcalculation[j] = calculation
            subcleanraw[j] = raw
            subresult[j] = result  
    
    # Remove any failed runs (None entries)
    subcalculation = [item for item in subcalculation if item is not None]
    subcleanraw = [item for item in subcleanraw if item is not None]
    subresult = [item for item in subresult if item is not None]
    
   #if no plates processed return message and none
    if len(subcalculation) == 0:
        print("Warning: No plates were successfully processed.")
        return None

    #Add plate name column and combine result in DataFrames
    subcalculation = {name: subcalculation[i] for i, name in enumerate(data[:len(subcalculation)])}
    subcleanraw = {name: subcleanraw[i] for i, name in enumerate(data[:len(subcleanraw)])}
    subresult = {name: subresult[i] for i, name in enumerate(data[:len(subresult)])}

    # Add 'plate_name' to each DataFrame in 'subresult'
    for name, df in subresult.items():
        df['plate_name'] = name
    fullresult = pd.concat(subresult.values(), ignore_index=True)

    for name, df in subcalculation.items():
        df['plate_name'] = name
    fullcalc = pd.concat(subcalculation.values(), ignore_index=True)

    return {
        'combined_calculation': fullcalc,
        'combined_cleanraw': subcleanraw,
        'combined_result': fullresult
    }

#Example: Run fill pipeline from raw files
if __name__ == "__main__":
    grinder_data = BulkReadMARS(path = '.././tutorials/data/grinder/', plate_subfix = 'plate', raw_subfix = 'raw')

    params = {
        'CleanMeta': {
            'split_content': True,
            'split_into': ['dilution', 'sampleID']
        },
        'GetCalculation': {
            'norm': True,
            'norm_ct': 'pos',
            'sd_fold': 10,
            'cycle_background': 6
        },
        'GetAnalysis': {
            'control': 'neg',
            'alternative': 'greater'
        },
        'SummarizeResult': {
            'sig_method': 'metric_count',
            'method_threshold': 3
        }
    }

    results = BulkProcessing(
        data = grinder_data,
        params = params,
        verbose = True)