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
        ## Calculating Delta-V
        """
        ),
        html.Div(
            id = 'div_4',
            style={'marginBottom': 10, 'marginTop': 10}
        ),
        dcc.Markdown(
        """
        In order to travel from one body to another in space we must produce a change in velocity (delta-v).
        The required delta-v for a mission can be found by using a porkchop plot, which shows contours of
        required delta-v against combinations of launch date and arrival date for a particular interplanetary trajectory
        """
        ),
        dcc.Markdown(
        """ **Select Mission Origin and Destination**"""
        ),
        html.Div(
            id = 'div_2',
            children = [
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
                        {'label': 'Venus', 'value': 'venus'},
                        {'label': 'Jupiter', 'value': 'jupiter'},
                        {'label': 'Saturn', 'value': 'saturn'},
                    ],
                    value='mars'
                ),
            ],
            style={'marginBottom': 10, 'marginTop': 10}
        ),
        html.Div(
            id = 'div_4',
            style={'marginBottom': 5, 'marginTop': 30}
        ),
        dcc.Markdown(
        """ **Configure the X-axis**"""
        ),
        dcc.Markdown(
        """ Select a starting date. This date will serve as the minimum value on the X-axis"""
        ),
        dcc.DatePickerSingle(
            id = 'minimum_mission_start_date',
            min_date_allowed = '2000-01-01',
            max_date_allowed = '2049-12-31',
            initial_visible_month = '2020-04-01',
            date = '2020-04-01'
        ),
    ], width = 4
)


column2 = dbc.Col([
        html.Div(
        id = 'graph_div',
        children = [
            dcc.Graph(
                id = 'plot',
                figure = create_pork_chop_plot(dt(2020, 4, 1).date(),
                                               dt(2020, 10, 1).date()),
                config = {'displayModeBar': False},
            ),
            dcc.Slider(
                id = 'range_slider',
                min=1,
                max=10,
                marks={i: '{} Years'.format(i) for i in range(10)},
                value=.6,
            ),
            dcc.Markdown(
            """ This slider will change the scale of the x axis. WARNING: Large date ranges will increase load time"""
            ),
        ]),
    ], width = 8
)


@app.callback(
    Output('plot', 'figure'),
    [Input('minimum_mission_start_date', 'date'),
    Input('range_slider', 'value'),
    Input('origin_body', 'value'),
    Input('arival_body', 'value')],
    [State('plot', 'figure')])
def update_plot(min_date, year_range, origin, destination, figure):
    # Date parsing
    parsed_start_date = dt.strptime(min_date, '%Y-%m-%d').date()
    parsed_end_date = parsed_start_date + timedelta(days = (365 * year_range))

    # Create plot
    fig = create_pork_chop_plot(parsed_start_date,
                                parsed_end_date,
                                origin,
                                destination)
    return fig


layout = dbc.Row([column1, column2])
