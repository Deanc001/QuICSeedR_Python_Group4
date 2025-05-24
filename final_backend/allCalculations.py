import pandas as pd
from QUICSEEDDASH.ConvertTime import convert_time
from QUICSEEDDASH.GetReplicate import get_replicate
from QUICSEEDDASH.CleanMeta import clean_meta
from QUICSEEDDASH.CleanRaw import clean_raw
from QUICSEEDDASH.GetCalculation import get_calculation
from QUICSEEDDASH.SpreadCalculation import spread_calculation
from QUICSEEDDASH.GetAnalysis import get_analysis
from QUICSEEDDASH.SummarizeResult import summarize_result

# All the calculations that aren't visible to the user in the same order they are executed in R studio

# Delete this block if everything is loaded in a different way
plate_96 = pd.read_excel('20240716_s1_plate.xlsx')
raw_96 = pd.read_excel('20240716_s1_raw.xlsx')
plate_384 = pd.read_excel('20230808_M12_plate.xlsx')
raw_384 = pd.read_excel('20230808_M12_raw.xlsx')

# Actual calculations start from here
plate_time_96 = convert_time(raw_96)
plate_time_384 = convert_time(raw_384)

replicate_96 = get_replicate(plate_96)
replicate_384 = get_replicate(plate_384)

meta_96 = clean_meta(raw_96, plate_96, replicate_96)
meta_384 = clean_meta(raw_384, plate_384, replicate_384)

cleanraw_96 = clean_raw(meta_96, raw_96, plate_time_96)
cleanraw_384 = clean_raw(meta_384, raw_384, plate_time_384)

calculation_96 = get_calculation(cleanraw_96, meta_96, norm=True, norm_ct='Pos')
calculation_384 = get_calculation(cleanraw_384, meta_384, norm=True, norm_ct='pos')

calculation_spread_96 = spread_calculation(calculation_96, terms=['RAF'])

analysis_96 = get_analysis(calculation_spread=calculation_spread_96, control='Neg', test='wilcox',
                           alternative='greater', alpha=0.05)


# This is the final step which should be implemented using a button or smth like that. Leaving it here just for the correct order
summary_result_96 = summarize_result(analysis=analysis_96, calculation=calculation_96, sig_method='RAF')