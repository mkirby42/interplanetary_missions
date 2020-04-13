"""
from datetime import datetime as dt
from datetime import timedelta
import pykep as pk
import numpy as np
from scipy import array
import pandas as pd
import copy

from .index import create_pork_chop_plot

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from pykep.core import epoch, DAY2SEC, lambert_problem, propagate_lagrangian, SEC2DAY, AU, ic2par


from app import app


def get_orbit(planet, date):

    planet = pk.planet.jpl_lp(planet)
    epoch_ = epoch(date)

    T = planet.compute_period(epoch_) * SEC2DAY
    N = 300
    when = np.linspace(0, T, N)

    x = np.array([0.0] * N)
    y = np.array([0.0] * N)
    z = np.array([0.0] * N)

    for i, day in enumerate(when):
        r, v = planet.eph(epoch(date + day))
        x[i] = r[0] / AU
        y[i] = r[1] / AU
        z[i] = r[2] / AU

    return [x, y, z]


def get_plot_data(day):
    return_dict = {}

    plnts = {'mercury': '#7C7C7C',
             'venus': '#DFE0A8',
             'earth': '#42B3EF',
             'mars': '#DA5C2E',
             'jupiter': '#F89B10',
             'saturn': '#E3CA4E',
             #'uranus': '#37EBE2',
             #'neptune': '#3740EB'
             }

    for planet in plnts:
        orb_data = get_orbit(planet, day)
        return_dict[planet] = {
        'orbit':{'x':orb_data[0], 'y':orb_data[1], 'z':orb_data[2]},
        'position':{'x':[orb_data[0][0]], 'y':[orb_data[1][0]], 'z':[orb_data[2][0]]},
        'color': plnts[planet]}

    return return_dict


def generate_solar_system(day):
    planets = get_plot_data(day)

    # Create Orbits
    fig_data = [go.Scatter3d(
        x = planets[planet]['orbit']['x'],
        y = planets[planet]['orbit']['y'],
        z = planets[planet]['orbit']['z'],
        marker = dict(
            size = .1,
            color = planets[planet]['color'],
        ),
    ) for planet in planets]

    # Create moving planets
    fig_frames = []
    N = 300
    for k in range(N):
        fig_frames.append(go.Frame(data=[
        go.Scatter3d(
            x = [planets[planet]['orbit']['x'][k]],
            y = [planets[planet]['orbit']['y'][k]],
            z = [planets[planet]['orbit']['z'][k]],
            marker = dict(
                size = 5,
                color = planets[planet]['color'],
            )
        ) for planet in planets]
        ))

    fig_data = fig_data + [
        go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            opacity=1,
            marker=dict(
                size=7,
                color= '#ECEF42',
            ),
        )
    ]

    new_data = copy.deepcopy(fig_data)

    fig = go.Figure(
        data = new_data + fig_data,
        layout = dict(
            title_text = "The Solar System",
            updatemenus = [dict(
                type = "buttons",
                buttons = [dict(
                    label = "Play",
                    method = "animate",
                    args = [None]
                    )]
            )]),
        frames = fig_frames
    )


    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks = 5, range = [-15, 15],),
                     yaxis = dict(nticks = 5, range = [-15, 15],),
                     zaxis = dict(nticks = 5, range = [-5, 5],),),
        height = 600,
        width = 1200,
        showlegend = False
    )


    fig.update_layout(
        scene = dict(
            xaxis = dict(
                 backgroundcolor="black",
                 gridcolor="black",
                 showbackground=True,
                 zerolinecolor="black",),
            yaxis = dict(
                backgroundcolor="black",
                gridcolor="black",
                showbackground=True,
                zerolinecolor="black"),
            zaxis = dict(
                backgroundcolor="black",
                gridcolor="black",
                showbackground=True,
                zerolinecolor="black",)
                )

    )

    camera = dict(
    up=dict(x=0, y=1, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=.06, y=.06, z=.009)
    )

    fig.update_layout(scene_camera = camera)

    return fig


layout = dcc.Graph(
    id = 'plot',
    figure = generate_solar_system(day = 7400),
    config = {'displayModeBar': False},
)

"""
