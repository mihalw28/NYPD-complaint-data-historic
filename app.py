import dash
from dash.dependencies import Input, Output, State, Event
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
    df['days'] = df.index.strftime('%y-%m-%d')
    df['hours'] = df.index.strftime('%H:%M')
    # make additional df
    pivot_df = df.pivot(index='days', columns='hours', values='pedestrians')
    pivot_data_temperatures = df.pivot(index='days', columns='hours', values='temperature')
    pivot_data_precipitation = df.pivot(index='days', columns='hours', values='precipitation')
    df.drop(['days', 'hours'], 1, inplace=True)   
    totalList = []
    for month in df.groupby(df.index.month):
        dailyList = []
        for day in month[1].groupby(month[1].index.day):
            dailyList.append(day[1])
        totalList.append(dailyList)
    return np.array(totalList), pivot_df, pivot_data_temperatures, pivot_data_precipitation

totalList, pivot_df, pivot_data_temperatures, pivot_data_precipitation = initialize()


hours = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', 
         '6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
         '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
xlist = list(hours)
ylist = list(pivot_df.index)
zlist =[]
for row in pivot_df.iterrows():
    index, data = row
    zlist.append(data.tolist())

#pivot_temps
def pivot_temperatures():
    zlist_temps = []
    for row in pivot_data_temperatures.iterrows():
        index, data4 = row
        zlist_temps.append(data4.tolist())
    z_temps=[]
    for i in range(0, len(zlist_temps)):
        z_temps.append(np.mean(zlist_temps[i]))
    return z_temps

z_temps = pivot_temperatures()

#pivot_precip
def pivot_precipitation():
    zlist_prec = []
    for row in pivot_data_precipitation.iterrows():
        index, data5 = row
        zlist_prec.append(data5.tolist())  
    z_prec=[]
    for i in range(0, len(zlist_prec)):
        z_prec.append(np.sum(zlist_prec[i]))
    return z_prec

z_prec = pivot_precipitation()


app.layout = html.Div([
    html.Div([
        html.H2('A simple analysis of pedestrian traffic on Brooklyn Bridge.',
            style = {'font-family': 'Montserrat'},
            className='title eight columns'
        )
    ],
    className='row'
    ),
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='parent-tabs',
        className='custom-tabs-container ten columns offset-by-one', 
        children=[
            dcc.Tab(
                label='Play',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    html.Div([
                        html.Div([
                            dcc.Slider(
                                min=0,
                                max=4,
                                value=0,
                                marks={i: ''.format(i + 1) for i in range(5)},
                                id='slider',
                                included=False,
                                className='slider two columns offset-by-five'
                            ),
                        ],
                        #className='row',
                        style={'margin-bottom': '10px'}
                        ),

                    ],
                    ),
                    html.Div([
                        dcc.Markdown(
                            id='text',
                            className='three columns offset-by-one'
                        ),
                        html.Div([
                            html.Button('Back', id='back', style={
                                        'display': 'inline-block'}),
                            html.Button('Next', id='next', style={
                                        'display': 'inline-block'})
                        ],
                        className='two columns offset-by-five'
                        ),
                    ],
                    className='row',
                    style={'margin-bottom': '10px'}
                    ),
                    dcc.Graph(
                        id='graph',
                        style={'height': 700},
                        className='ten columns offset-by-one'
                    ),
                ],
            ),
            dcc.Tab(
                label='Explore',
                className='custom-tab', 
                selected_className='custom-tab--selected',
                children=[
                    html.Div([
                        dcc.Markdown(
                            '''
                            ### Title
                            '''.replace('  ', ''),
                            className='eight columns offset-by-two'
                        )
                    ],
                    className='row',
                    style={'text-align': 'center', 'margin-bottom': '15px',
                        'margin-top': '20px'}
                    ),
                    html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id='month-picker',
                                options=[
                                    {'label': "Oct '17", 'value': 'oct'},
                                    {'label': "Nov '17", 'value': 'nov'},
                                    {'label': "Dec '17", 'value': 'dec'},
                                    {'label': "Jan '18", 'value': 'jan'},
                                    {'label': "Feb '18", 'value': 'feb'},
                                    {'label': "Mar '18", 'value': 'mar'},
                                    {'label': "Apr '18", 'value': 'apr'},
                                    {'label': "May '18", 'value': 'may'},
                                    {'label': "Jun '18", 'value': 'jun'},
                                    {'label': "Jul '18", 'value': 'jul'},
                                ],
                                value='oct',
                                multi=True,
                                className='two columns', 
                            ),
                            dcc.Graph(
                                id='example-graph-1',
                                figure={
                                    'data': [
                                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                                            'type': 'bar', 'name': 'SF'},
                                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                                            'type': 'bar', 'name': u'Montréal'},
                                    ]
                                },
                                className='six columns',
                            ),
                            dcc.Graph(
                                id='radar-chart',
                                className='six columns offset-by-six'
                            ),
                        ],
                        className='row'
                        )
                    ]),
                    html.Div([
                        dcc.Graph(
                                id='scatter-plot',
                                className='twelve columns'
                            ),
                    ],
                    className='row'
                    )
                ]  
            ),
        ]
    ),
    html.Div(id='tabs-content-classes')
])

# Internal logic
last_back = 0
last_next = 0

UPS = {
    0: dict(x=1, y=0, z=1),
    1: dict(x=0, y=0, z=1),
    2: dict(x=0, y=0, z=1),
    3: dict(x=0, y=0, z=1),
    4: dict(x=0, y=0, z=1),
    
}

CENTERS = {
    0: dict(x=0.3, y=0.8, z=-0.5),
    1: dict(x=0, y=0, z=-0.37),
    2: dict(x=0, y=1.1, z=-1.3),
    3: dict(x=0, y=-0.7, z=0),
    4: dict(x=0, y=-0.2, z=0),
    
}

EYES = {
    0: dict(x=2.7, y=2.7, z=0.3),
    1: dict(x=0.01, y=3.8, z=-0.37),
    2: dict(x=1.3, y=3, z=0),
    3: dict(x=2.6, y=-1.6, z=0),
    4: dict(x=3, y=-0.2, z=0),
    
}

TEXTS = {
    0: '''
    ##### INTRO
    This raph shows the total number of pedestrians visiting Brooklyn Brigde over 9 months. 
    Measurements started from october '17. Data covers the range until July '18.
    '''.replace('  ', ''),
    1: '''
    ##### INTRO 2
    The chart shows the changing numbers of pedestrians depending on the time of day,
    seasons or day of the week.
    '''.replace('  ', ''),
    2: '''
    ##### EVENTS
    Particular attention is paid to the values that stand out clearly against the
    background of the immediate environment. We can count New Year's Eve together
    with the New Year.
    '''.replace('  ', ''),
    3: '''
    ##### SEASONAL FLUCTUATIONS
    Statistically the highest pedestrian traffic volume is visible in the case of
    good, stable weather in warmer months.
    '''.replace('  ', ''),
    4: '''
    ##### WEATHER IMPACT
    In this graph you can see the impact of the weather and especially its rapid changes
    on the number of Brooklyn Bridge visitors.
    '''.replace('  ', '')
}

ANNOTATIONS = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
}



# Make 3d graph
@app.callback(Output('graph', 'figure'), [Input('slider', 'value')])
def make_graph(value):

    if value is None:
        value = 0

    if value in range(0, 4):
        trace1 = go.Surface(
            x=xlist,
            y=ylist,
            z=np.array(zlist),
            hoverinfo='x+y+z',
            lighting=dict(
                ambient=0.95, 
                diffuse=0.95, 
                roughness = 0.01, 
                specular=0, 
                fresnel=0.02,
            ),
            colorscale='Viridis',
            opacity=1.0,
        )

        data = [trace1]

        layout = go.Layout(
            paper_bgcolor="#efefef",
            title='Brooklyn Brodge pedestrians - 3-D view.',
            autosize=True,
            font=dict(
                size=12,
                color='#090B11',
            ),
            margin=dict(
                t=30,
                l=50,
                b=30,
                r=50,
            ),
            showlegend=False,
            hovermode='closest',
            scene=dict(
                aspectmode="manual",
                aspectratio=dict(x=2.5, y=5, z=1.5),
                camera=dict(
                    up=UPS[value],
                    center=CENTERS[value],
                    eye=EYES[value]
                ),
                xaxis=dict(
                    backgroundcolor="#efefef",
                    showbackground=True,
                    title="",
                    showgrid=True,
                    zeroline=True,
                    tickvals=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22],
                    ticktext=['0:00', '2:00', '4:00', '6:00', '8:00', '10:00',
                              '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'],
                    tickfont=dict(
                        color='#090B11',
                        size=12,
                        family='Old Standard TT, serif',
                    ),
                    nticks=12,
                    autorange='reversed',
                    zerolinecolor='black', #change
                    zerolinewidth=4, #change
                ),
                yaxis=dict(
                    backgroundcolor="#efefef",
                    showbackground=True,
                    showgrid=False,
                    title="",
                    tickfont=dict(
                        color='#090B11',
                        size=12,
                        family='Old Standard TT, serif',
                    ),
                    zeroline=True,
                    zerolinecolor='black', #change
                    zerolinewidth=4, #change

                ),
                zaxis=dict(
                    backgroundcolor="#efefef",
                    showbackground=True,
                    showgrid=True,
                    title="",
                    nticks=7,
                    tickvals=[0, 100, 500, 1000, 2000, 3000, 4000],
                    tickfont=dict(
                        color='#090B11',
                        size=12,
                        family='Old Standard TT, serif',
                    ),
                ),
            ),
        )
    else:
        trace1 = go.Heatmap(
            zsmooth='best',
            x=ylist,
            y=xlist,
            z=np.array(zlist).T,
            colorscale='Viridis',
            name='yaxis1 data',
            yaxis='y1',
        )
        trace2 = go.Scatter(
            x=ylist,
            y=z_prec,
            name='yaxis2 data',
            yaxis='y2',
            line = dict(
                color=('#ffa600'),
                width =1
            ),
            showlegend=False
        )
        trace3 = go.Scatter(
            x=ylist,
            y=z_temps,
            name='yaxis3 data',
            yaxis='y3',
            line=dict(
                color=('#f95d6a'),
                width=1,
            ),
            showlegend=False
        )

        data = [trace1, trace2, trace3]

        layout = go.Layout(
            title='Double Y Axis Example',
            titlefont=dict(
                color='#090B11',
                family='Montserrat, bold',
                size=18,
            ),
            paper_bgcolor="#efefef",
            xaxis=dict(
                tickfont=dict(
                        color='#090B11',
                        size=12,
                        family='Raleway, regular',
                    ),
            ),
            yaxis=dict(
                tickfont=dict(
                        color='#090B11',
                        size=12,
                        family='Raleway',
                    ),
            ),
            yaxis2=dict(
                overlaying='y',
                side='left',
                range=[0.0,5],
                ticks='',
                showticklabels=False
            ),
            yaxis3=dict(
                overlaying='y',
                side='right',
                range=[8.0, 150],
                ticks='',
                showticklabels=False
            )
        )

    figure = go.Figure(data=data, layout=layout)
    return figure


# Make annotations
@app.callback(Output('text', 'children'), [Input('slider', 'value')])
def make_text(value):
    if value is None:
        value = 0
    return TEXTS[value]


# Button controls
@app.callback(Output('slider', 'value'),
              [Input('back', 'n_clicks'), Input('next', 'n_clicks')],
              [State('slider', 'value')])
def advance_slider(back, nxt, slider):

    if back is None:
        back = 0
    if nxt is None:
        nxt = 0
    if slider is None:
        slider = 0

    global last_back
    global last_next

    if back > last_back:
        last_back = back
        return max(0, slider - 1)
    if nxt > last_next:
        last_next = nxt
        return min(5, slider + 1)

external_css = [
    "//fonts.googleapis.com/css?family=Montserrat|Raleway:Regular",
]

for css in external_css:
    app.css.append_css({"external_url": css})

# Run the Dash app
if __name__ == '__main__':
    app.server.run()