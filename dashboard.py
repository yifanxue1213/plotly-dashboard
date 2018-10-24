import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.graph_objs import layout as plotlyLayout
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
                # slider
                html.Div([
                    dcc.Slider(
                        id='bin-slider',
                        min=1,
                        max=60,
                        step=1,
                        value=20,
                        updatemode='drag'
                    ),
                ], className='histogram-slider'),
                html.P('# of Bins: Auto', id='bin-size', className='bin-size'),
                html.Div([
                    dcc.Checklist(
                        id='bin-auto',
                        options=[
                            {'label': 'Auto', 'value': 'Auto'}
                        ],
                        values=['Auto']
                    ),
                ], className='bin-auto'),
                    dcc.Graph(id='dynamic-power'),
                ], className='dynamic-power'),
                # histogram of power
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

    trace = Scatter(
        y=df['Speed'],
        mode='markers'
    )

    layout = Layout(
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
        margin=plotlyLayout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


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

    trace = Scatter(
        y=df['Speed'],
        line=scatter.Line(
            color='#990000'
        ),
        mode='lines'
    )

    layout = Layout(
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
        margin=plotlyLayout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


# Callback for power update
@app.callback(Output('dynamic-power', 'figure'),
              [Input('dynamic-power-update', 'n_intervals')],
              [State('bin-slider', 'value'),
               State('bin-auto', 'values')])
def get_power(interval, sliderValue, auto_state):
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

    # plot histogram
    wind_val = df['Speed']
    if 'Auto' in auto_state:
        bin_val = np.histogram(wind_val, bins=range(int(round(min(wind_val))),
                                                    int(round(max(wind_val)))))
    else:
        bin_val = np.histogram(wind_val, bins=sliderValue)

    avg_val = float(sum(wind_val)) / len(wind_val)
    median_val = np.median(wind_val)

    pdf_fitted = rayleigh.pdf(bin_val[1], loc=(avg_val) * 0.55,
                              scale=(bin_val[1][-1] - bin_val[1][0]) / 3)

    y_val = pdf_fitted * max(bin_val[0]) * 20,
    y_val_max = max(y_val[0])
    bin_val_max = max(bin_val[0])

    trace = Bar(
        x=bin_val[1],
        y=bin_val[0],
        marker=bar.Marker(
            color='#7F7F7F'
        ),
        showlegend=False,
        hoverinfo='x+y'
    )
    trace1 = Scatter(
        x=[bin_val[int(len(bin_val) / 2)]],
        y=[0],
        mode='lines',
        line=scatter.Line(
            dash='dash',
            color='#2E5266'
        ),
        marker=scatter.Marker(
            opacity=0,
        ),
        visible=True,
        name='Average'
    )
    trace2 = Scatter(
        x=[bin_val[int(len(bin_val) / 2)]],
        y=[0],
        line=scatter.Line(
            dash='dot',
            color='#BD9391'
        ),
        mode='lines',
        marker=scatter.Marker(
            opacity=0,
        ),
        visible=True,
        name='Median'
    )
    trace3 = Scatter(
        mode='lines',
        line=scatter.Line(
            color='#42C4F7'
        ),
        y=y_val[0],
        x=bin_val[1][:len(bin_val[1])],
        name='Rayleigh Fit'
    )
    layout = Layout(
        xaxis=dict(
            title='Wind Speed (mph)',
            showgrid=False,
            showline=False,
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            title='Number of Samples',
            fixedrange=True
        ),
        margin=plotlyLayout.Margin(
            t=50,
            b=20,
            r=50
        ),
        autosize=True,
        bargap=0.01,
        bargroupgap=0,
        hovermode='closest',
        legend=plotlyLayout.Legend(
            x=0.175,
            y=-0.2,
            orientation='h'
        ),
        shapes=[
            dict(
                xref='x',
                yref='y',
                y1=int(max(bin_val_max, y_val_max)) + 0.5,
                y0=0,
                x0=avg_val,
                x1=avg_val,
                type='line',
                line=plotlyLayout.shape.Line(
                    dash='dash',
                    color='#2E5266',
                    width=5
                )
            ),
            dict(
                xref='x',
                yref='y',
                y1=int(max(bin_val_max, y_val_max)) + 0.5,
                y0=0,
                x0=median_val,
                x1=median_val,
                type='line',
                line=plotlyLayout.shape.Line(
                    dash='dot',
                    color='#BD9391',
                    width=5
                )
            )
        ]
    )
    return Figure(data=[trace, trace1, trace2, trace3], layout=layout)

# for histogram slider
@app.callback(Output('bin-auto', 'values'), [Input('bin-slider', 'value')],
              [State('dynamic-power', 'figure')],
              [Event('bin-slider', 'change')])
def deselect_auto(sliderValue, wind_speed_figure):
    if (wind_speed_figure is not None and
       len(wind_speed_figure['data'][0]['y']) > 5):
        return ['']
    else:
        return ['Auto']

# for histogram slider
@app.callback(Output('bin-size', 'children'), [Input('bin-auto', 'values')],
              [State('bin-slider', 'value')],
              [])
def deselect_auto(autoValue, sliderValue):
    if 'Auto' in autoValue:
        return '# of Bins: Auto'
    else:
        return '# of Bins: ' + str(int(sliderValue))


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

    trace = Scatter(
        y=df['Speed'],
        line=scatter.Line(
            color='#990000'
        ),
        mode='lines'
    )

    layout = Layout(
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
        margin=plotlyLayout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    return Figure(data=[trace], layout=layout)


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