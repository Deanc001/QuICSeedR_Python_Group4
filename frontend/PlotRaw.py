import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import plotly.graph_objects as go
from plotly.colors import qualitative
import pandas as pd
import numpy as np
import anvil.server
import anvil.plotly_templates
from plotly.subplots import make_subplots

@anvil.server.callable
def cleanraw_default_settings (sample = None, xlim= None, ylim= None, title= None, xlab= None, ylab= None):
   if sample is None:
     sample = ['bl_', 'Neg_', 'Pos_', 'V5_', 'M5_', 'D5_', 'L5_',
       'V6_', 'M6_', 'D6_', 'L6_']
   
   if title is None: 
     title = "Fluorescence vs Time (h)"
   if xlab is None:
     xlab="Time (h)"
   if ylab is None:
     ylab="Fluorescence"
   return sample, title, xlim, ylim,  xlab, ylab
  
@anvil.server.callable
def cleanraw_please_plot(sample = None, chart_name = None,
                           xlim=None, ylim=None,
                           xlab=None, ylab=None, ): 


  
  raw = pd.read_csv(data_files['cleanraw_96.csv'], nrows=10000)
  if sample is None:
    sample = ['bl_', 'Neg_', 'Pos_', 'V5_', 'M5_', 'D5_', 'L5_',
      'V6_', 'M6_', 'D6_', 'L6_']  
 
  sample_tuple = tuple(sample)
  fig = plot_raw_single_plotly(raw, sample_tuple, chart_name, xlim, ylim, xlab, ylab)

  return fig

def plot_raw_single_plotly(raw, sample, chart_name,
                           xlim, ylim, xlab, ylab, custom_colors = None,
                           linetypes=None, legend_position = 'top left'):
  

    time = np.array(raw.index, dtype=float)

    # Select relevant columns
    sel = [j for j, col_name in enumerate(raw.columns) if col_name.startswith(sample)]
    name_array = [col_name for col_name, col_name in enumerate(raw.columns) if col_name.startswith(sample) ]

    # Determine y-axis limits
    if ylim is None:
        ymax = np.nanmax(raw.iloc[:, sel].values)
        ylim = (0, ymax / 0.8)

    # Determine x-axis limits
    if xlim is None:
        xlim = (np.nanmin(time), np.nanmax(time))

    if xlab is None:
      xlab = 'Time (h)'
      
    if ylab is None:
      ylab = 'Fluoresence'

    if chart_name is None:
      chart_name = 'Fluoresence vs Time (h)'

 
    
