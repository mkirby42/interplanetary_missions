#index
from datetime import datetime as dt
import datetime
import pykep as pk
import numpy as np
from scipy import array
import pandas as pd

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
            # Why Go To Space?
            """
        ),
        html.Div(
            id = 'div_4',
            style={'marginBottom': 25, 'marginTop': 25}
        ),
        dcc.Markdown(
            """
            Humanity rolls the dice with extinction every day.

            Any day could be our last as a species; it would take an event of
            epic proportions, a truly global catastrophe. However, history shows
            us that global catastrophes, while rare, occur with alarming
            regularity.

            If Humanity wishes to survive for longer than what amounts to a
            cosmic rounding error, we must expand beyond our home planet.
            An entire universe beckons, but alas space is hard.
            """
        ),
        dcc.Link(dbc.Button("Let's Get Started", color='primary'), href='/first_steps')
    ], width = 5,
)


column2 = dbc.Col(
    [
        html.Img(id = 'image', src = 'assets/missle_row.jpg', width = 650, height = 500)
    ], width = 7
)




layout = [dbc.Row([column1, column2])]
