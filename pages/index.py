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

def create_pork_chop_plot(start_date, end_date, origin = 'earth', destination = 'mars'):

    # Epoch range (x axis)
    initial_epoch_date = datetime.date(2000, 1, 1)

    start_epoch = float((start_date - initial_epoch_date).days)
    end_epoch = float((end_date - initial_epoch_date).days)
    start_epochs = np.arange(start_epoch, end_epoch, 1.0)

    # Time of flight (y axis)
    duration = np.arange(50.0, 500.0, 3.0)

    # Origin
    origin_planet = pk.planet.jpl_lp(origin)
    # Destination
    destination_planet = pk.planet.jpl_lp(destination)

    data = list()
    for start in start_epochs:
        row = list()
        for T in duration:
            r1,v1 = origin_planet.eph(pk.epoch(start, 'mjd2000'))
            r2,v2 = destination_planet.eph(pk.epoch(start+T, 'mjd2000'))
            l = pk.lambert_problem(r1, r2, T*60*60*24, pk.MU_SUN)
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
            line_width  = 1,
            colorbar = dict(
                title = 'Delta V (m/s)', # title here
                titleside = 'right',
                titlefont = dict(
                    family = "Courier New, monospace",
                    size = 18,
                    color = "#7f7f7f"
                    )
            ),
            hovertemplate = "Launch Date: %{x}<br>" +
                "Time of Flight: %{y} Days<br>" +
                "Delta-V: %{z:.0f} m/s<br>",
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
            # Why Go To Space?
            """
        ),
        html.Div(
            id = 'div_4',
            style={'marginBottom': 25, 'marginTop': 25}
        ),
        dcc.Markdown(
            """
            Humanity roles the dice with extinction every day.

            Any day could be our last as a species; it would take an event of
            epic proportions, a truly global catastrophe. However, history shows
            us that global catastrophes, while rare, occur with alarming
            regularity.

            If Humanity wishes to survive for longer than what ammounts to a
            cosmic rounding error, we must expand beyond our home planet. An
            entire universe bekons, but alas space is hard.
            """
        ),
    ], width = 5,
)


column2 = dbc.Col(
    [
        dcc.Graph(id = 'plot',
            figure = create_pork_chop_plot(dt(2020, 4, 1).date(),
                                           dt(2020, 10, 1).date()),
            config = {'displayModeBar': False},
        ),
    ],
)




layout = [dbc.Row([column1, column2])]
