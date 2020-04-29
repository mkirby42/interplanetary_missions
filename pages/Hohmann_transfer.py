from datetime import datetime as dt
from datetime import timedelta
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


def settle_mars(launches_day, max_dv, max_tof, isru, mass):
    months_in_year = 12
    window_occurance = 26
    days_in_window = 30
    pop = 100000
    payload_to_surface = 150000

    total_mass = mass * pop
    reduced_mass = total_mass - (total_mass * (isru / 100))
    launches_needed = reduced_mass / payload_to_surface
    launches_per_window = launches_day * days_in_window
    windows_needed = launches_needed / launches_per_window
    years_needed = windows_needed * window_occurance / months_in_year

    return years_needed



column1 = dbc.Col(
    [
        dcc.Markdown(
        """
        Select the number of launches per day.
        """
        ),
        dcc.Slider(
            id = 'launches_per_day_slider',
            min = 0,
            max = 30,
            marks = {i: '{}'.format(i) for i in range(0, 30, 3)},
            value = 1,
        ),
        dcc.Markdown(
        """
        Select the maximum delta-v our missions can achieve.
        """
        ),
        dcc.Slider(
            id = 'max_delta_v_slider',
            min = 0,
            max = 10000,
            marks = {i: '{} m/s'.format(i) for i in range(0, 10000, 2500)},
            value = 2500,
        ),
        dcc.Markdown(
        """
        Select the maximum acceptable time of flight.
        """
        ),
        dcc.Slider(
            id = 'max_tof_slider',
            min = 0,
            max = 500,
            marks = {i: '{} days'.format(i) for i in range(0, 500, 100)},
            value = 300,
        ),
        dcc.Markdown(
        """
        Select the ISRU reduction factor.
        """
        ),
        dcc.Slider(
            id = 'isru_slider',
            min = 0,
            max = 100,
            marks = {i: '{} %'.format(i) for i in range(0, 100, 10)},
            value = 10,
        ),
        dcc.Markdown(
        """
        Select the required mass per settler.
        """
        ),
        dcc.Slider(
            id = 'mass_per_person_slider',
            min = 0,
            max = 20000,
            marks = {i: '{} Kg'.format(i) for i in range(0, 20000, 5000)},
            value = 17000,
        ),
    ])


column2 = dbc.Col(
    [
    html.Div(id = 'launches_per_day', children = "Launches Per Day: 1"),
    html.Div(id = 'max_delta_v', children = "Maximum Delta-V: 2500 m/s"),
    html.Div(id = 'max_tof', children = "Maximum Time of Flight: 300 Days"),
    html.Div(id = 'isru', children = "ISRU Reduction Factor: 10%"),
    html.Div(id = 'mass_per_person', children = "Mass Per Settler: 2000 Tons"),
    html.Div(id = 'equation', children = "Years to Settle Mars: ")
    ]
)


@app.callback(
    Output('launches_per_day', 'children'),
    [Input('launches_per_day_slider', 'value')]
)
def show_launches_per_day(input):
    return "Launches Per Day: "+ str(input)


@app.callback(
    Output('max_delta_v', 'children'),
    [Input('max_delta_v_slider', 'value')]
)
def show_max_delta_v(input):
    return "Maximum Delta-V: "+ str(input) + " m/s"


@app.callback(
    Output('max_tof', 'children'),
    [Input('max_tof_slider', 'value')]
)
def show_max_tof(input):
    return "Maximum Time of Flight: "+ str(input) + " Days"


@app.callback(
    Output('isru', 'children'),
    [Input('isru_slider', 'value')]
)
def show_isru(input):
    return "ISRU Reduction Factor: "+ str(input) + "%"


@app.callback(
    Output('mass_per_person', 'children'),
    [Input('mass_per_person_slider', 'value')]
)
def show_mpp(input):
    return "Mass Per Settler: "+ str(input) + " Tons"


@app.callback(
    Output('equation', 'children'),
    [
    Input('launches_per_day_slider', 'value'),
    Input('max_delta_v_slider', 'value'),
    Input('max_tof_slider', 'value'),
    Input('isru_slider', 'value'),
    Input('mass_per_person_slider', 'value')
    ]
)
def show_equation(launches_day, max_dv, max_tof, isru, mass):
    years = settle_mars(launches_day, max_dv, max_tof, isru, mass)
    return f"How Long to Settle Mars: {years} Years"


layout = dbc.Row([column1, column2])
