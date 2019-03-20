import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.plotly as py
import plotly.graph_objs as go
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import pandas as pd
import os
import pymysql

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
            html.H3("Voltages (V)")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='dynamic-voltage'),
        ], className='twelve columns dynamic-temp'),
        dcc.Interval(id='dynamic-voltage-update', interval=1000, n_intervals=0),
    ], className='row dynamic-line-row'),
    html.Div([
        html.Div([
            html.Div([
                html.H3("Ave Voltages (V)")
            ], className='Title'),
            html.Div(id='ave-voltage'),
            dcc.Interval(id='realtime-average-voltage-update', interval=1000, n_intervals=0),
        ], className='six columns dynamic-line-row'),
        html.Div([
            html.Div([
                html.H3("RPM")
            ], className='Title'),
            html.Div(id='rpm-value'),
            dcc.Interval(id='realtime-rpm-update', interval=1000, n_intervals=0),
        ], className='six columns dynamic-line-row'),
    ], className='row wind-histo-polar'),
    html.Div([
        html.Div([
            html.H3("Operating Current (A)")
        ], className='Title'),
        html.Div([
            dcc.Graph(id='dynamic-op-current'),
        ], className='twelve columns dynamic-op-current'),
        dcc.Interval(id='dynamic-op-current-update', interval=1000, n_intervals=0),
    ], className='row dynamic-line-row'),
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "75%",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


# Callback for temp update
@app.callback(Output('dynamic-temp', 'figure'), [Input('dynamic-temp-update', 'n_intervals')])
def get_temp(interval):
    con = pymysql.connect(host='localhost',
                                 port= 8889,
                                 user='uscsolar',
                                 password='solarcar',
                                 db='uscsolarcar',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql_query("SELECT temp1, temp2, temp3, temp4," +
                           " temp5, temp6, temp7, temp8," +
                           " temp9, temp10, temp11, temp12," +
                           " temp13, temp14, temp15, temp16," +
                           " temp17, temp18, temp19, temp20," +
                           " temp21, temp22, temp23, temp24," +
                           " from temporature ORDER BY id DESC LIMIT 1;", con)
    con.close()

    layout = go.Layout(
        height=450,
        xaxis=dict(
            title='Temperature Sensors'
        ),
        yaxis=dict(
            # range=[min(0, min(df['Speed'])),
            #        max(45, max(df['Speed'])+max(df['SpeedError']))],
            range=[30, 150],
            showline=False,
            fixedrange=True,
            zeroline=False
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    numOfTempSensors = 24
    uscRed = 'rgba(142, 26, 17, 1)'
    normalBlue = 'rgba(54, 119, 175, 1)'
    colors = [normalBlue] * numOfTempSensors
    tempLowerBound = 60
    tempUpperBound = 95

    xLabels = []
    valueList = []
    for i in range(0, numOfTempSensors):
        tmpInd = "temp" + str(i + 1)
        tempLable = "t" + str(i + 1)
        if (df[tmpInd][0] < tempLowerBound) or (df[tmpInd][0] > tempUpperBound):
            colors[i] = uscRed
        else:
            colors[i] = normalBlue
        xLabels.append(tempLable)
        valueList.append(df[tmpInd][0])

    trace = go.Bar(
        x=xLabels,
        y=valueList,
        hoverinfo='y',
        text=valueList,
        textposition='auto',
        marker=dict(
            color=colors
        ),
    )

    return go.Figure(data=[trace], layout=layout)


# Callback for voltage update
@app.callback(Output('dynamic-voltage', 'figure'), [Input('dynamic-voltage-update', 'n_intervals')])
def get_voltage(interval):
    con = pymysql.connect(host='localhost',
                                 port= 8889,
                                 user='uscsolar',
                                 password='solarcar',
                                 db='uscsolarcar',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql_query("SELECT voltage1, voltage2, voltage3, voltage4," +
                           " voltage5, voltage6, voltage7, voltage8," +
                           " voltage9, voltage10, voltage11, voltage12," +
                           " voltage13, voltage14, voltage15, voltage16," +
                           " voltage17, voltage18, voltage19, voltage20," +
                           " voltage21, voltage22, voltage23, voltage24," +
                           " voltage25, voltage26, voltage27, voltage28," +
                           " from voltage ORDER BY id DESC LIMIT 1;", con)
    con.close()

    layout = go.Layout(
        height=450,
        xaxis=dict(
            title='Voltage Sensors'
        ),
        yaxis=dict(
            range=[min(0, min(df['voltage'])),
                   max(5, max(df['voltage']))],
            showline=False,
            fixedrange=True,
            zeroline=False
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )

    numOfTempSensors = 28
    uscRed = 'rgba(142, 26, 17, 1)'
    normalBlue = 'rgba(54, 119, 175, 1)'
    colors = [normalBlue] * numOfTempSensors
    tempLowerBound = 2.5
    tempUpperBound = 4.5

    xLabels = []
    valueList = []
    for i in range(0, numOfTempSensors):
        tmpInd = "voltage" + str(i + 1)
        tempLable = "v" + str(i + 1)
        if (df[tmpInd][0] < tempLowerBound) or (df[tmpInd][0] > tempUpperBound):
            colors[i] = uscRed
        else:
            colors[i] = normalBlue
        valueList.append(df[tmpInd][0])
        xLabels.append(tempLable)

    trace = go.Bar(
        x=xLabels,
        y=valueList,
        hoverinfo='y',
        text=valueList,
        textposition='auto',
        marker=dict(
            color=colors
        ),
    )

    return go.Figure(data=[trace], layout=layout)

# Callback for rpm update
@app.callback(Output(component_id='ave-voltage', component_property='children'),
    [Input('realtime-average-voltage-update', 'n_intervals')])
def update_rpm(interval):
    # get voltages
    con = pymysql.connect(host='localhost',
                          port=8889,
                          user='uscsolar',
                          password='solarcar',
                          db='uscsolarcar',
                          charset='utf8',
                          cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql_query("SELECT voltage1, voltage2, voltage3, voltage4," +
                           " voltage5, voltage6, voltage7, voltage8," +
                           " voltage9, voltage10, voltage11, voltage12," +
                           " voltage13, voltage14, voltage15, voltage16," +
                           " voltage17, voltage18, voltage19, voltage20," +
                           " voltage21, voltage22, voltage23, voltage24," +
                           " voltage25, voltage26, voltage27, voltage28," +
                           " from voltage ORDER BY id DESC LIMIT 1;", con)
    con.close()
    ave = df.mean(axis=1)
    return '{}'.format(ave[0])

# Callback for rpm update
@app.callback(Output(component_id='rpm-value', component_property='children'),
    [Input('realtime-rpm-update', 'n_intervals')])
def update_rpm(interval):
    # get new rpm
    con = pymysql.connect(host='localhost',
                          port=8889,
                          user='uscsolar',
                          password='solarcar',
                          db='uscsolarcar',
                          charset='utf8',
                          cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql_query('SELECT rpm from motor ORDER BY id DESC LIMIT 1;', con)
    con.close()

    return '{}'.format(df['rpm'][0])


# Callback for operating current update
@app.callback(Output('dynamic-op-current', 'figure'), [Input('dynamic-op-current-update', 'n_intervals')])
def get_opcurrent(interval):

    con = pymysql.connect(host='localhost',
                          port=8889,
                          user='uscsolar',
                          password='solarcar',
                          db='uscsolarcar',
                          charset='utf8',
                          cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql_query('SELECT current from workCondition ORDER BY id DESC LIMIT 200;', con)
    con.close()

    trace = go.Scatter(
        y=df['current'],
        line= go.scatter.Line(
            color='#990000'
        ),
        mode='lines'
    )

    layout = go.Layout(
        height=450,
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            title='Time Elapsed (sec)'
        ),
        yaxis=dict(
            range=[min(0, min(df['current'])),
                   max(4, max(df['current']))],
            showline=False,
            fixedrange=True,
            zeroline=False,
            nticks=max(6, round(df['current'].iloc[-1]/10))
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