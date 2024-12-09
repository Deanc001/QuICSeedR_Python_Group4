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
def metric_default_settings (sample = None, xlim= None, ylim= None, title= None, xlab= None, ylab= None):
  if sample is None:
    sample = ['bl_', 'Neg_', 'Pos_', 'V5_', 'M5_', 'D5_', 'L5_',
       'V6_', 'M6_', 'D6_', 'L6_']
     
  if title is None: 
     title = "Plate Plot"
       
  if xlab is None:
     xlab="Content"
    
  if ylab is None:
     ylab="Selected Threshold Metric"
  
  return sample, title, xlim, ylim,  xlab, ylab

@anvil.server.callable
def metric_please_plot (sample = None, chart_name = None,
                           xlim=None, ylim=None,
                           xlab=None, ylab=None):
  raw = pd.read_csv(data_files['calculation_raw_96.csv'], nrows=10000)
  if chart_name is None:
    chart_name = 'Metric Plot'
  if xlab is None:
    xlab = "Content"
  if ylab is None:
    ylab = "Selected Threshold Metric"
  
  fig = plot_metric_plotly(raw, chart_name, xlab, ylab)
  return fig

@anvil.server.callable
def plot_metric_plotly(calculation, chart_name, xlab, ylab, x="content", y="RAF", fill_var=None,
                       point=True, box=True):
    fig = go.Figure()
   
    print("Available columns in calculation:", calculation.columns)
    print(f"x: {x}, y: {y}, xlab: {xlab}, ylab: {ylab}")

    # Add boxplot if enabled
    if box:
        fig.add_trace(go.Box(
            x=calculation[x],
            y=calculation[y],
            
            name="Boxplot",
            boxmean='sd',  # Display mean and standard deviation
            marker_color='gray',
            opacity=0.7
        ))

    # Add scatter points if enabled
    if point:
        fig.add_trace(go.Scatter(
            x=calculation[x],
            y=calculation[y],
            mode='markers',
            name="Points",
            marker=dict(color='blue', opacity=0.8)
        ))

    # Update layout
    print ('here??')
    fig.update_layout(
        title=chart_name,
        xaxis_title=xlab if xlab else xlab.capitalize(),
        yaxis_title=ylab if ylab else ylab.capitalize(),
        xaxis=dict(tickangle=45),
        template='plotly_white'
    )

    fig.show()
    return fig
