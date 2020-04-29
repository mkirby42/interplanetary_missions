import pykep as pk
from pykep.core import epoch, propagate_lagrangian, SEC2DAY, AU
import numpy as np
import pandas as pd

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

from app import app


def get_orbit(planet, day):
    planet = pk.planet.jpl_lp(planet)
    epoch_ = epoch(day)

    T = planet.compute_period(epoch_) * SEC2DAY
    N = int(round(T))
    when = np.linspace(0, T, N)

    x = np.array([0.0] * N)
    y = np.array([0.0] * N)
    z = np.array([0.0] * N)

    for i, day in enumerate(when):
        r, v = planet.eph(epoch(epoch_.mjd2000 + day))
        x[i] = r[0] / AU
        y[i] = r[1] / AU
        z[i] = r[2] / AU

    return x, y, z


def get_lambert_pos(l):
    sol = 0
    N = 200

    # We extract the relevant information from the Lambert's problem
    r = l.get_r1()
    v = l.get_v1()[sol]
    l_tof = l.get_tof()
    mu = l.get_mu()
    # We define the integration time ...
    dt = l_tof / (N - 1)
    # ... and alocate the cartesian components for r
    l_x = np.array([0.0] * N)
    l_y = np.array([0.0] * N)
    l_z = np.array([0.0] * N)
    # We calculate the spacecraft position at each dt
    for i in range(N):
        l_x[i] = r[0] / AU
        l_y[i] = r[1] / AU
        l_z[i] = r[2] / AU
        r, v = propagate_lagrangian(r, v, dt, mu)
    return l_x, l_y, l_z


def add_t(x, y, z, fig, size = .1, color = 'white'):
    fig.add_trace(go.Scatter3d(x = x, y = y, z = z,
    opacity = 1,
    marker = dict(
        size = size,
        color = color,
    ),
    ))


start_date = 7305.0
end_date = 7671.0
intervals = 1.0
start_epochs = np.arange(start_date, end_date, intervals)
max_tof = 400.0
duration = np.arange(120.0, max_tof, 1.0)
origin = 'earth'
destination = 'mars'
earth = pk.planet.jpl_lp(origin)
mars = pk.planet.jpl_lp(destination)
data = list()

for start in start_epochs:
    row = list()

    for tof in duration:

        pos_1, v1 = earth.eph(pk.epoch(start, 'mjd2000'))
        pos_2, v2 = mars.eph(pk.epoch(start + tof, 'mjd2000'))

        seconds_elapsed = tof * 60 * 60 * 24 if tof > 0 else 1 * 60 *60 * 24

        l = pk.lambert_problem(pos_1, pos_2, seconds_elapsed, pk.MU_SUN)

        DV1 = np.linalg.norm(np.array(v1) - np.array(l.get_v1()[0]) )
        DV2 = np.linalg.norm(np.array(v2) - np.array(l.get_v2()[0]) )

        DV1 = max([0, DV1 - 4000])
        DV = DV1+DV2

        row.append(DV)

    data.append(row)


minrows = [min(l) for l in data]
i_idx = np.argmin(minrows) # Index of minimum value
j_idx = np.argmin(data[i_idx])
best = data[i_idx][j_idx] / 1000

start = start_date
tof = duration[j_idx]

pos_1, v1 = earth.eph(pk.epoch(start_epochs[i_idx], 'mjd2000'))
pos_2, v2 = mars.eph(pk.epoch(start_epochs[i_idx] + tof, 'mjd2000'))

seconds_elapsed = tof * 60 * 60 * 24 if tof > 0 else 1 * 60 *60 * 24

l = pk.lambert_problem(pos_1, pos_2, seconds_elapsed, pk.MU_SUN)

e_x, e_y, e_z = get_orbit('earth', 7350)
m_x, m_y, m_z = get_orbit('mars', 7700)
l_x, l_y, l_z = get_lambert_pos(l)

orbit_fig = go.Figure(data = [
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
])

add_t(e_x, e_y, e_z, orbit_fig, size = .1, color = 'blue')
add_t(m_x, m_y, m_z, orbit_fig, size = .1, color = 'red')
add_t(l_x, l_y, l_z, orbit_fig, size = .1, color = 'white')
add_t([pos_1[0] / AU], [pos_1[1] / AU], [pos_1[2] / AU], orbit_fig, size = 5, color = 'blue')
add_t([pos_2[0] / AU], [pos_2[1] / AU], [pos_2[2] / AU], orbit_fig, size = 3, color = 'red')

orbit_fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=4, range=[-6,6],),
        yaxis = dict(nticks=4, range=[-6,6],),
        zaxis = dict(nticks=4, range=[-10,10],),))

orbit_fig.update_layout(showlegend=False)

camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=.2, y=.2, z=.1)
)

orbit_fig.update_layout(scene_camera = camera)
orbit_fig.update_layout(
    title={
        'text': "Hohmann Transfer Orbit",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
orbit_fig.update_layout(scene = dict(
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
                        zerolinecolor="black",),),
                  )

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
        ),
        hovertemplate = "Launch Date: %{x}<br>" +
            "Time of Flight: %{y} Days<br>" +
            "Delta-V: %{z:.0f} m/s<br>",
    ))

fig.update_layout(
    xaxis_title = "Departure Date",
    yaxis_title = "Time of Flight (Days)",
    height = 400,
)

fig.update_layout(
    title={
        'text': origin.title() + " -> " + destination.title(),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

launch_epoch = pk.epoch(int(start_epochs[i_idx]))
tof = duration[j_idx]
arival_epoch = start_epochs[i_idx] + tof

best_dv_string = "Best Delta-V: " + str(best) + " Km/s"
launch_date_string = "Launch Date: " +  str(launch_epoch)[:-8]
tof_string = "Duration: " +  str(tof) + ' Days'

column1 = dbc.Col(
    [
        dcc.Markdown(
        """
        ## Our First Steps
        """
        ),
        html.Div(
            id = 'div_4',
            style={'marginBottom': 10, 'marginTop': 10}
        ),
        dcc.Markdown(
        """
        Mars is the closest celestial body that could feasibly support an
        independent branch of human civilization, but getting there is no cakewalk.

        To travel from one body to another in space we must produce a change in velocity (delta-v).
        The required delta-v for a mission can be found using a porkchop plot, which shows contours of
        required delta-v against combinations of the launch date and arrival date for a particular interplanetary trajectory

        Optimal launch windows between Earth and Mars occur every 26 months
        with flight times as low as 100 days. The time of flight is
        not only dependant on the relative positions of the two planets, but also
        the performance of our spacecraft. A more powerful spacecraft
        can achive a higher delta-v.

        One of the most efficient ways to get from one orbit to another in
        space is to use a Hohmann transfer orbit. A Hohmann transfer orbit,
        named after Walter Hohmann, uses two impulses: one to move onto the
        transfer orbit and another to move off of it. Hohmann was a German
        scientist inspired by science fiction; he first published work on the
        orbit in his 1925 book Die Erreichbarkeit der Himmelskörper
        (The Attainability of Celestial Bodies).

        """
        ),
        html.Div(
            id = 'div_4',
            style={'marginBottom': 5, 'marginTop': 30}
        ),
        dcc.Markdown(
        best_dv_string
        ),
        dcc.Markdown(
        launch_date_string
        ),
        dcc.Markdown(
        tof_string
        ),
    ], width = 5
)


column2 = dbc.Col([
        html.Div(
        id = 'graph_div',
        children = [
            dcc.Graph(
                id = 'plot',
                figure = fig,
                config = {'displayModeBar': False},
            ),
            dcc.Graph(
                id = 'orbit',
                figure = orbit_fig,
                config = {'displayModeBar': False},
            ),
        ]),
    ], width = 7
)



layout = dbc.Row([column1, column2])
