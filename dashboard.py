import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
import plotly.graph_objs as go
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import pandas as pd
import os
import sqlite3
import datetime as dt

app = dash.Dash('Solar-Car-Monitor-Dashboard')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H2("Solar Car Monitor Dashboard"),
        html.Img(src="./assets/img/solcar.png"),
    ], className='banner'),
    html.Div([
        html.Div([
            html.H3("Temperature (F)")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='dynamic-temp'),
        ], className='twelve columns dynamic-temp'),
        dcc.Interval(id='dynamic-temp-update', interval=1000, n_intervals=0),
    ], className='row dynamic-line-row'),
    html.Div([
        html.Div([
            html.Div([
                html.H3("Voltages (V)")
            ], className='Title'),
            html.Div([
                dcc.Graph(id='dynamic-voltage'),
            ], className='dynamic-voltage'),
            dcc.Interval(id='dynamic-voltage-update', interval=1000, n_intervals=0),
        ], className='six columns dynamic-line-row'),
        html.Div([
            html.Div([
                html.H3("Power (W)")
            ], className='Title'),
            html.Div([
                dcc.Graph(id='dynamic-power'),
            ], className='dynamic-power'),
            dcc.Interval(id='dynamic-power-update', interval=1000, n_intervals=0),
        ], className='six columns dynamic-line-row')
    ], className='row wind-histo-polar'),
    html.Div([
        html.Div([
            html.H3("Speed (M/H)")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='dynamic-speed'),
        ], className='twelve columns dynamic-speed'),
        dcc.Interval(id='dynamic-speed-update', interval=1000, n_intervals=0),
    ], className='row dynamic-line-row'),
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "75%",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


# Callback for temp update
@app.callback(Output('dynamic-temp', 'figure'), [Input('dynamic-temp-update', 'n_intervals')])
def get_temp(interval):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("./Data/wind-data.db")
    df = pd.read_sql_query('SELECT Speed, SpeedError, Direction from Wind where\
                            rowid > "{}" AND rowid <= "{}";'
                            .format(total_time-200, total_time), con)

    layout = go.Layout(
        height=450,
        xaxis=dict(
            title='Temperature Sensors'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    numOfTempSensors = 3
    uscRed = 'rgba(142, 26, 17, 1)'
    normalBlue = 'rgba(54, 119, 175, 1)'
    colors = [normalBlue] * numOfTempSensors
    tempLowerBound = 8
    tempUpperBound = 20

    for i in range(0, numOfTempSensors):
        if (df['Speed'][i] < tempLowerBound) or (df['Speed'][i] > tempUpperBound):
            colors[i] = uscRed
        else:
            colors[i] = normalBlue
    trace = go.Bar(
        x=['c3','b2','a1'],
        y=[df.iloc[-3]['Speed'],df.iloc[-2]['Speed'],df.iloc[-1]['Speed']],
        hoverinfo='y',
        text=[df.iloc[-3]['Speed'],df.iloc[-2]['Speed'],df.iloc[-1]['Speed']],
        textposition='auto',
        marker=dict(
            color=colors
        ),
    )

    return go.Figure(data=[trace], layout=layout)


# Callback for voltage update
@app.callback(Output('dynamic-voltage', 'figure'), [Input('dynamic-voltage-update', 'n_intervals')])
def get_voltage(interval):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("./Data/wind-data.db")
    df = pd.read_sql_query('SELECT Speed, SpeedError, Direction from Wind where\
                            rowid > "{}" AND rowid <= "{}";'
                            .format(total_time-200, total_time), con)

    trace = go.Scatter(
        y=df['Speed'],
        line= go.scatter.Line(
            color='#990000'
        ),
        mode='lines'
    )

    layout = go.Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return go.Figure(data=[trace], layout=layout)


# Callback for power update
@app.callback(Output('dynamic-power', 'figure'),
              [Input('dynamic-voltage-update', 'n_intervals')])
def get_power(interval):
    # get power data
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("./Data/wind-data.db")
    df = pd.read_sql_query('SELECT Speed, SpeedError, Direction from Wind where\
                                rowid > "{}" AND rowid <= "{}";'
                           .format(total_time - 200, total_time), con)

    trace = go.Scatter(
        y=df['Speed'],
        line= go.scatter.Line(
            color='#990000'
        ),
        mode='lines'
    )

    layout = go.Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return go.Figure(data=[trace], layout=layout)


# Callback for speed update
@app.callback(Output('dynamic-speed', 'figure'), [Input('dynamic-speed-update', 'n_intervals')])
def get_temp(interval):
    now = dt.datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour

    total_time = (hour * 3600) + (minute * 60) + (sec)

    con = sqlite3.connect("./Data/wind-data.db")
    df = pd.read_sql_query('SELECT Speed, SpeedError, Direction from Wind where\
                            rowid > "{}" AND rowid <= "{}";'
                            .format(total_time-200, total_time), con)

    trace = go.Scatter(
        y=df['Speed'],
        line= go.scatter.Line(
            color='#990000'
        ),
        mode='lines'
    )

    layout = go.Layout(
        height=450,
        xaxis=dict(
            range=[0, 200],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            tickvals=[0, 50, 100, 150, 200],
            ticktext=['200', '150', '100', '50', '0'],
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(df['Speed'])),
                   max(45, max(df['Speed'])+max(df['SpeedError']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return go.Figure(data=[trace], layout=layout)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "./assets/css/streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                'https://codepen.io/chriddyp/pen/bWLwgP.css' # for Tab
                ]


for css in external_css:
    app.css.append_css({"external_url": css})

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

if __name__ == '__main__':
    app.run_server()