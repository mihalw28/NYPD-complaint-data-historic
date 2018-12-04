import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
from flask_cors import CORS
import numpy as np
import pandas as pd
import os


external_stelesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stelesheets)
server = app.server


#Pull data and make array
def initialize():
    df = pd.read_csv('https://s3.amazonaws.com/brooklyn-bridge-pedestrians/brooklyn_bridge_data.csv')
    df.drop('Unnamed: 0', 1, inplace=True)
    df['hour_beginning'] = pd.to_datetime(df['hour_beginning'], format='%Y-%m-%d %H:%M:%S')
    df.index = df['hour_beginning']
    df.drop('hour_beginning', 1, inplace=True)
    totalList = []
    for month in df.groupby(df.index.month):
        dailyList = []
        for day in month[1].groupby(month[1].index.day):
            dailyList.append(day[1])
        totalList.append(dailyList)
    return np.array(totalList)



app.layout = html.Div([
    html.H1('App demo with 2 tabs'),
    dcc.Tabs(id='tabs-example', value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)