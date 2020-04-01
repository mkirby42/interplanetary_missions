#index
from datetime import datetime as dt
import datetime
import pygmo as pg
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

def create_pork_chop_plot(start_date, end_date, origin = 'earth', destination = 'mars'):

    # Epoch range (x axis)
    initial_epoch_date = datetime.date(2000, 1, 1)

    start_epoch = float((start_date - initial_epoch_date).days)
    end_epoch = float((end_date - initial_epoch_date).days)
    start_epochs = np.arange(start_epoch, end_epoch, 1.0)

    # Time of flight (y axis)
    duration = np.arange(180.0, 470.0, 1.0)

    # Origin
    earth = pk.planet.jpl_lp(origin)
    # Destination
    mars = pk.planet.jpl_lp(destination)

    data = list()
    for start in start_epochs:
        row = list()
        for T in duration:
            r1,v1 = earth.eph(pk.epoch(start, 'mjd2000'))
            r2,v2 = mars.eph(pk.epoch(start+T, 'mjd2000'))
            l = pk.lambert_problem(r1, r2, T*60*60*24, earth.mu_central_body)
            DV1 = np.linalg.norm(np.array(v1) - np.array(l.get_v1()[0]))
            DV2 = np.linalg.norm(np.array(v2) - np.array(l.get_v2()[0]))
            DV1 = max([0, DV1 - start_epoch])
            DV = DV1 + DV2
            row.append(DV)
        data.append(row)

    minrows = [min(l) for l in data]
    i_idx = np.argmin(minrows)
    j_idx = np.argmin(data[i_idx])

    duration_pl, start_epochs_pl = np.meshgrid(duration, start_epochs)

    date_series = pd.to_datetime([i[0] for i in start_epochs_pl],
        unit='d',
        origin=pd.Timestamp('2000-01-01')
        )

    date_vals = [str(i)[:10] for i in date_series.values]

    fig = go.Figure(data =
        go.Contour(
            z = np.array(data).T,
            x = date_vals, # horizontal axis
            y = duration_pl[0], # vertical axis
            colorscale = 'thermal',
            contours = dict(
                start = data[i_idx][j_idx],
                end = 7000,
                size = 100,
            ),
            xcalendar = 'julian',
            contours_coloring = 'lines',
            line_width  =1,
            colorbar = dict(
                title = 'Delta V (m/s)', # title here
                titleside = 'right',
                titlefont = dict(
                    family = "Courier New, monospace",
                    size = 18,
                    color = "#7f7f7f"
                    )
            ),
        ))
    fig.update_layout(
        xaxis_title = "Departure Date",
        yaxis_title = "Time of Flight (Days)",
        font = dict(
            family = "Courier New, monospace",
            size = 18,
            color = "#7f7f7f"
        ),
        height = 500,
    )

    fig.update_layout(
        title={
            'text': origin.title() + " -> " + destination.title(),
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig



column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Porkchop Plots

            A porkchop plot (also pork-chop plot) is a chart that shows contours of equal characteristic energy (C3) against combinations of launch date and arrival date for a particular interplanetary flight.

            By examining the results of the porkchop plot, engineers can determine when launch opportunities exist (a launch window) that is compatible with the capabilities of a particular spacecraft. A given contour, called a porkchop curve, represents constant C3, and the center of the porkchop the optimal minimum C3. The orbital elements of the solution, where the fixed values are the departure date, the arrival date, and the length of the flight, were first solved mathematically in 1761 by Johann Heinrich Lambert, and the equation is generally known as Lambert's problem (or theorem). -Wikipedia
            """
        ),
    ],
    md=4,
)


column2 = dbc.Col(
    [
        dcc.Graph(id = 'plot',
            figure = create_pork_chop_plot(dt(2020, 4, 1).date(),
                                           dt(2020, 10, 1).date())
        ),
    ],
)




layout = [dbc.Row([column1, column2])]
