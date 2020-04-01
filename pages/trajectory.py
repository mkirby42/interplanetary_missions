#index
from datetime import datetime as dt
import pygmo as pg
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
        html.Div(
            id = 'div_2',
            style={'marginBottom': 75, 'marginTop': 50}
        ),
        dcc.Markdown(
        """#### Create a timeframe for the plot"""
        ),
        html.Div(
            id = 'div_2',
            style={'marginBottom': 25, 'marginTop': 25}
        ),
        dcc.DatePickerSingle(
            id = 'minimum_mission_start_date',
            min_date_allowed = '2000-01-01',
            max_date_allowed = '2049-12-31',
            initial_visible_month = '2020-04-01',
            date = '2020-04-01'
        ),
        dcc.DatePickerSingle(
            id = 'maximum_mission_end_date',
            min_date_allowed = '2000-01-02',
            max_date_allowed = '2050-01-01',
            initial_visible_month = '2021-01-01',
            date = '2021-01-01'
        ),
        html.Div(
            id = 'div_2',
            style={'marginBottom': 50, 'marginTop': 25}
        ),
        dcc.Markdown(
        """#### Select an origin and destination for the mission"""
        ),
        html.Div(
            id = 'div_2',
            style={'marginBottom': 25, 'marginTop': 25}
        ),
        dcc.Dropdown(
            id = 'origin_body',
            options=[
                {'label': 'Earth', 'value': 'earth'},
            ],
            value='earth'
        ),
        dcc.Dropdown(
            id = 'arival_body',
            options=[
                {'label': 'Mars', 'value': 'mars'},
            ],
            value='mars'
        ),
    ],
    md = 4
)


column2 = dbc.Col([
        dcc.Graph(id = 'plot',
            figure = create_pork_chop_plot(dt(2020, 4, 1).date(),
                                           dt(2020, 10, 1).date())
        ),
    ]
)


@app.callback(
    Output('plot', 'figure'),
    [Input('minimum_mission_start_date', 'date'),
    Input('maximum_mission_end_date', 'date'),
    Input('origin_body', 'value'),
    Input('arival_body', 'value')],
    [State('plot', 'figure')])
def update_plot(min_date, max_date, origin, destination, figure):
    # Date parsing
    parsed_start_date = dt.strptime(min_date, '%Y-%m-%d').date()
    parsed_end_date = dt.strptime(max_date, '%Y-%m-%d').date()

    # Create plot
    fig = create_pork_chop_plot(parsed_start_date,
                                parsed_end_date,
                                origin,
                                destination)
    return fig


layout = dbc.Row([column1, column2])
