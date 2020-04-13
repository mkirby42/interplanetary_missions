from datetime import datetime as dt
from datetime import timedelta
import pykep as pk
import numpy as np
from scipy import array
import pandas as pd

from .index import create_pork_chop_plot

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
        """
        ## Earth Mars Transfer
        """
        )
    ])

layout = dbc.Row([column1])
