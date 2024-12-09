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
def plate_default_settings (sample = None, title= None, xlim= None, ylim= None, xlab = None, ylab = None):
  if sample is None:
    sample = ['bl_', 'Neg_', 'Pos_', 'V5_', 'M5_', 'D5_', 'L5_',
       'V6_', 'M6_', 'D6_', 'L6_']
     
  if title is None: 
     title = "Plate Plot"
  
  return sample, title, xlim, ylim, xlab, ylab

@anvil.server.callable
def plate_please_plot (sample = None, chart_name = None,
                           xlim=None, ylim=None,
                           xlab = None, ylab = None):
   raw = pd.read_csv(data_files['raw_96.csv'], nrows=10000)
   time = pd.read_csv(data_files['plate_time_96.csv'], nrows=10000)
   raw = raw.apply(pd.to_numeric, errors='coerce')
   
   fig = plot_plate (raw, time, chart_name, xlab, ylab, )
   return fig

def plot_plate(raw, plate_time, chart_name, xlab, ylab,  format=96, f_size=10):
    if format == 96:
        rows = [chr(i) for i in range(ord('A'), ord('H') + 1)]
        cols = [f"{i:02}" for i in range(1, 13)]
        n_row, n_col = 8, 12
    elif format == 384:
        rows = [chr(i) for i in range(ord('A'), ord('P') + 1)]
        cols = [f"{i:02}" for i in range(1, 25)]
        n_row, n_col = 16, 24
    else:
        raise ValueError("Invalid format. Must be either 96 or 384.")

    y_min, y_max = np.inf, -np.inf
    for well in raw.columns:
        y_min = min(y_min, raw[well].min())
        y_max = max(y_max, raw[well].max())


    if chart_name is None:
      chart_name = 'Fluoresence vs Time for each Well '
    
    fig = go.Figure()
  

    fig = make_subplots(
        rows=n_row, cols=n_col,
        shared_xaxes=True, shared_yaxes=True,
        vertical_spacing=0.02, horizontal_spacing=0.02
    )

    time = plate_time.iloc[:, 0].values
  
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            well = f"{row}{col}"
            if well in raw.columns:
                y_data = raw[well].values
                trace = go.Scatter(x=time, y=y_data, mode='lines', line=dict(width=1), showlegend=False)
                fig.add_trace(trace, row=n_row - i, col=j + 1)
            fig.update_yaxes(range=[y_min, y_max], row=i + 1, col=j + 1)


    annotations = []
    

    for i, row_label in enumerate(rows):
        annotations.append(dict(
            x=-0.05, y=(n_row - i - 0.5) / n_row,
            xref="paper", yref="paper",
            text=row_label,
            showarrow=False,
            font=dict(size=f_size, color="black")
        ))

    for j, col_label in enumerate(cols):
        annotations.append(dict(
            x=(j + 0.5) / n_col, y=1.05,
            xref="paper", yref="paper",
            text=col_label,
            showarrow=False,
            font=dict(size=f_size, color="black")
        ))
    
    


    fig.update_layout(
        title=dict(text=chart_name, x=0.5),
        height=1200,
        width=1600,
        showlegend=False,
        margin=dict(l=50, r=20, t=50, b=50),
        annotations=annotations
    )

    fig.update_xaxes(title_text=" ", row=n_row, col=1)
    fig.update_yaxes(title_text=" ", row=1, col=1)

    fig.show()

    return fig
