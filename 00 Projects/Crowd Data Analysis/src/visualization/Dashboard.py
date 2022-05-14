#import libraries
import numpy as np                                                      #for fast operations on arrays    
import pandas as pd                                                     #for read & manipulate dataset
import plotly.express as px                                             #for Data visualization
import plotly.figure_factory as ff                                      #for Data visualization
import dash                                                             #for Dashboard visualization
from dash import dcc                                                    #for Dashboard visualization
from dash import html                                                   #for Dashboard visualization
from dash.dependencies import Input, Output                             #for Dashboard visualization
import warnings
warnings.filterwarnings('ignore')

RSRP_DATA_PATH = '../../data/processed/RSRP_processed.parquet'
TRAFFICVOLUME_DATA_PATH = '../../data/processed/TrafficVolume_processed.parquet'

df_rsrp = pd.read_parquet(RSRP_DATA_PATH)
df_trafficvolume = pd.read_parquet(TRAFFICVOLUME_DATA_PATH)

#Dashboard
app = dash.Dash()

#Count Events per Radio Connection Type and opertators
snap4 = df_rsrp[['RadioOperatorName','RadioConnectionType']]
snap4['COUNTER'] =1 #initially, set that counter to 1.
snap4_filtered = pd.DataFrame(snap4.groupby(['RadioOperatorName','RadioConnectionType'])['COUNTER'].sum().reset_index())
Radio_Bar = px.bar(snap4_filtered, x="RadioOperatorName", y="COUNTER", color="RadioConnectionType")

#Count Events per Radio Genration Type and opertators
snap5 = df_rsrp[['RadioOperatorName','RadioNetworkGeneration']]
snap5['COUNTER'] =1                                     #initially, set that counter to 1.
snap5_filtered = pd.DataFrame(snap5.groupby(['RadioOperatorName','RadioNetworkGeneration'])['COUNTER'].sum().reset_index())
Genre_Bar = px.bar(snap5_filtered, x="RadioOperatorName", y="COUNTER", color="RadioNetworkGeneration")

#Count of events per hour
snap6 = df_rsrp[['Timestamp']]
snap6['Time'] = df_rsrp['Timestamp'].dt.strftime("%y-%m-%d %H")
snap6['Count'] = 1
snap6 = snap6[['Time','Count']].groupby('Time').count().reset_index()
event_hour = px.line(snap6, x='Time', y='Count' ,height=600)

#Get the most popular DeviceManufacturer
snap7 = pd.DataFrame(df_rsrp['DeviceManufacturer'].value_counts())
Manufacturer = px.bar(snap7, x="DeviceManufacturer", orientation='h',height=600)


app.layout = html.Div([
                        html.H1('4G Performance Dashboard'),

                        html.Div(id='row1',children=[
                            html.H2('Users Movement for all operators',style={}),
                            html.Div(dcc.Dropdown(id='Day',placeholder='Select Day', value= df_rsrp['Timestamp'].dt.day.unique()[0], options=[{'label': i, 'value': i} for i in df_rsrp['Timestamp'].dt.day.unique().tolist()],style={'width':'50%','margin-left':'10px'})),
                            html.Div(dcc.Graph(id='timelapse', config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),
                        
                       html.Div(id='row2',children=[
                            html.H2('Users Movement Per operator',style={}),
                            html.Div(dcc.Dropdown(id='Day_per_operator', value= df_rsrp['Timestamp'].dt.day.unique()[0], placeholder='Select Day',options=[{'label': i, 'value': i} for i in df_rsrp['Timestamp'].dt.day.unique().tolist()],style={'width':'50%','margin-left':'10px','margin-bottom':'10px'})),
                            html.Div(dcc.Dropdown(id='operator',placeholder='Select Operator', value= df_rsrp['RadioOperatorName'].unique()[0], options=[{'label': i, 'value': i} for i in df_rsrp['RadioOperatorName'].unique().tolist()],style={'width':'50%','margin-left':'10px'})),
                            html.Div(dcc.Graph(id='timelapse2', config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),
                        
                        html.Div(id='row3',children=[
                            html.H2('RSRP per device type per operator',style={}),
                            html.Div(dcc.Dropdown(id='aggregation', value ='Min', options=['Min', 'Max', 'Average','90th_Quantile'],placeholder='Select Aggregation Method',style={'width':'50%','margin-left':'10px','margin-bottom':'10px'})),
                            html.Div(dcc.Dropdown(id='RSRP_operator', value= df_rsrp['RadioOperatorName'].unique()[0], placeholder='Select Operator',options=[{'label': i, 'value': i} for i in df_rsrp['RadioOperatorName'].unique().tolist()],style={'width':'50%','margin-left':'10px'})),
                            html.Div(dcc.Graph(id='RSRP_Bar', config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),

                        html.Div(id='row4',children=[
                            html.H2('Downlink-Uplink traffic Volume per operator',style={}),
                            html.Div(dcc.Dropdown(id='direction',value= df_trafficvolume['TrafficDirection'].unique()[0], options=[{'label': i, 'value': i} for i in df_trafficvolume['TrafficDirection'].unique().tolist()] ,placeholder='Select Traffic Direction',style={'width':'50%','margin-left':'10px','margin-bottom':'10px'})),
                            html.Div(dcc.Dropdown(id='direction_operator', value= df_trafficvolume['RadioOperatorName'].unique()[0], placeholder='Select Operator',options=[{'label': i, 'value': i} for i in df_trafficvolume['RadioOperatorName'].unique().tolist()],style={'width':'50%','margin-left':'10px'})),
                            html.Div(dcc.Graph(id='traffic_map', config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),

                        html.Div(id='row5',children=[
                            html.H2('Most popular Devices Manufacturer',style={}),
                            html.Div(dcc.Graph(figure=Manufacturer, config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),

                        html.Div(id='row6',children=[
                            html.H2('Count Events per Radio Connection Type and opertators',style={}),
                            html.Div(dcc.Graph(figure=Radio_Bar, config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),

                        html.Div(id='row7',children=[
                            html.H2('Count Events per Radio Genration Type and opertators',style={}),
                            html.Div(dcc.Graph(figure=Genre_Bar, config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),
                        
                        html.Div(id='row8',children=[
                            html.H2('Count of events per hour',style={}),
                            html.Div(dcc.Graph(figure=event_hour, config= {'displaylogo': False}),style={})
                                                    ], style={'border':'1px solid black','border-radius': '10px','margin-bottom':'30px'}),

                       ],id='container',style={'margin':'100px'})


# time-lapse of a density map showing how users move during the hours of the day for all operators
@app.callback(
    Output(component_id='timelapse', component_property='figure'),
    [Input(component_id='Day', component_property='value')])

def Movement_alloperators(input_value):
    
    snap = df_rsrp[df_rsrp['Timestamp'].dt.day==input_value]
    snap['Timestamp']=snap['Timestamp'].dt.strftime('%H')
    fig  = px.density_mapbox(snap, lat='LocationLatitude', lon='LocationLongitude', z='RSRP', radius=10,
                        center=dict(lat=24.78054, lon=46.734737), zoom=9,animation_frame=sorted(snap['Timestamp']),
                        mapbox_style="stamen-terrain",height=700)

    fig.update_layout(transition_duration=500)
    return fig

# A heat map of user locations for a selected operator colored by RSRP value 
@app.callback(
    Output(component_id='timelapse2', component_property='figure'),
    [Input(component_id='Day_per_operator', component_property='value')],
    [Input(component_id='operator', component_property='value')])

def Movement_operator(input_value1,input_value2):
    snap = df_rsrp[(df_rsrp['RadioOperatorName']==input_value2) & (df_rsrp['Timestamp'].dt.day==input_value1)]
    snap['Timestamp']=snap['Timestamp'].dt.strftime('%H')
    fig = px.density_mapbox(snap, lat='LocationLatitude', lon='LocationLongitude', z='RSRP', radius=10,
                            center=dict(lat=24.78054, lon=46.734737), zoom=9, animation_frame=sorted(snap['Timestamp']),
                            mapbox_style="stamen-terrain",height=700)

    fig.update_layout(transition_duration=500)
    return fig


# A Bar chart of RSRP per device type per operator with an option to choose the aggregation method of RSRPe 
@app.callback(
    Output(component_id='RSRP_Bar', component_property='figure'),
    [Input(component_id='RSRP_operator', component_property='value')],
    [Input(component_id='aggregation', component_property='value')])

def RSRP_Operator_Device_aggergation(input_value1,input_value2):
    snap3 = df_rsrp[(df_rsrp['RadioOperatorName']==input_value1)]

    if input_value2 =='Min':
        snap3_filtered_min = snap3[['DeviceName','RSRP']].sort_values(['DeviceName','RSRP'],ascending = False).groupby('DeviceName').head(20).groupby('DeviceName').min()
        fig = px.bar(snap3_filtered_min, x="RSRP", height=500)
        fig.update_layout(transition_duration=500)

    elif input_value2 =='Max':
        snap3_filtered_max = snap3[['DeviceName','RSRP']].sort_values(['DeviceName','RSRP'],ascending = False).groupby('DeviceName').head(20).groupby('DeviceName').max()
        fig = px.bar(snap3_filtered_max, x="RSRP", height=500)
        fig.update_layout(transition_duration=500)

    elif input_value2 =='Average':
        snap3_filtered_average = snap3[['DeviceName','RSRP']].sort_values(['DeviceName','RSRP'],ascending = False).groupby('DeviceName').head(20).groupby('DeviceName').mean()
        fig = px.bar(snap3_filtered_average, x="RSRP", height=500)
        fig.update_layout(transition_duration=500)

    elif input_value2 =='90th_Quantile':
        snap3_filtered_quantile = snap3[['DeviceName','RSRP']].sort_values(['DeviceName','RSRP'],ascending = False).groupby('DeviceName').head(20).groupby('DeviceName').quantile(0.9)
        fig = px.bar(snap3_filtered_quantile, x="RSRP", height=500)
        fig.update_layout(transition_duration=500  )
    
    return fig


# visualize Downlink\Uplink traffic Volume
@app.callback(
    Output(component_id='traffic_map', component_property='figure'),
    [Input(component_id='direction', component_property='value')],
    [Input(component_id='direction_operator', component_property='value')])

def traffic_map(input_value1,input_value2):
    snap = df_trafficvolume[(df_trafficvolume['TrafficDirection']==input_value1) & (df_trafficvolume['RadioOperatorName']==input_value2) ]
    snap['Timestamp']=snap['Timestamp'].dt.strftime('%y-%m-%d %H:%M:%S')
    fig = ff.create_hexbin_mapbox(data_frame=snap, lat='LocationLatitude', lon='LocationLongitude',
                                    nx_hexagon=10, opacity=0.5, labels={"Volume": "TrafficVolume"},
                                    animation_frame = 'Timestamp',color='TrafficVolume',agg_func=np.sum,
                                    center=dict(lat=24.78054, lon=46.734737), zoom=8, mapbox_style="stamen-terrain",height=600)
    
    fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
    return fig  



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)