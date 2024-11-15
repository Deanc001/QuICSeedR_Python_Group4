import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
from Functions.ConvertTime import convert_time
from Functions.PlotPlate import plot_plate, interactive_plot_plate
from Functions.GetReplicate import get_replicate
from Functions.CleanMeta import clean_meta
from Functions.CleanRaw import clean_raw
from Functions.PlotRawMulti import plot_raw_multi
from Functions.PlotRawSingle import plot_raw_single
from Functions.GetCalculation import get_calculation
from Functions.PlotMetric import plot_metric
from Functions.SpreadCalculation import spread_calculation
from Functions.GetAnalysis import get_analysis
from Functions.SummarizeResult import summarize_result
from Functions.Operators import operators

pd.set_option("display.precision", 9)
pd.set_option('future.no_silent_downcasting', True)

plate_96 = pd.read_excel('data/20240716_s1_plate.xlsx')
raw_96 = pd.read_excel('data/20240716_s1_raw.xlsx')

plate_384 = pd.read_excel('data/20230808_M12_plate.xlsx')
raw_384 = pd.read_excel('data/20230808_M12_raw.xlsx')

plate_time_96 = convert_time(raw_96)
plate_time_384 = convert_time(raw_384)

replicate_96 = get_replicate(plate_96)
replicate_384 = get_replicate(plate_384)


meta_96 = clean_meta(raw_96, plate_96, replicate_96)
meta_384 = clean_meta(raw_384, plate_384, replicate_384)

cleanraw_96 = clean_raw(meta_96, raw_96, plate_time_96)
cleanraw_384 = clean_raw(meta_384, raw_384, plate_time_384)

#fig, axes = plt.subplots(1, 2, figsize=(15, 6))
#plot_raw_multi(cleanraw_96, ["Neg", "Pos"], custom_colors=["red"], ax=axes[0])
#plot_raw_single(cleanraw_384, "pos", ax=axes[1])
#plt.tight_layout()
#plt.show()

calculation_96 = get_calculation(cleanraw_96, meta_96, norm=True, norm_ct='Pos')
calculation_384 = get_calculation(cleanraw_384, meta_384, norm=True, norm_ct='pos')

"""
plot_metric(
    calculation=calculation_96,
    x="content",
    y="MS",
    point=True,
    box=True,
    boxplot={'palette': sns.color_palette("gray", n_colors=calculation_96['content'].nunique())},
    scatter={'palette': 'dark:blue'},
    xlab="Sample ID",
    ylab="Normalized Max Slope"
)
"""

calculation_spread_96 = spread_calculation(calculation_96, terms=['RAF'])

#rounded_spread_96 = calculation_spread_96['RAF'].round(2)
#print(tabulate(rounded_spread_96, headers='keys', tablefmt='pipe', showindex=False))

analysis_96 = get_analysis(calculation_spread=calculation_spread_96, control='Neg', test='wilcox',
                           alternative='greater', alpha=0.05)

#for term, df in analysis_96.items():
    #print(f"Results for {term}:")
    #df.index.name = None
    #print(tabulate(df, headers="keys", tablefmt="pipe", showindex=True))

summary_result_96 = summarize_result(analysis=analysis_96, calculation=calculation_96, sig_method='RAF')

#print(tabulate(summary_result_96, headers='keys', tablefmt='pipe', showindex=False))

#plot_plate(raw_96, plate_time_96)

"""""
interactive_fig = interactive_plot_plate(raw_384, plate_time_384, format=384)
interactive_fig.show()
"""""

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(replicate_96)
