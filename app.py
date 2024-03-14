import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json

data = pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/german-canteens(filtered).csv',sep='@', encoding='utf8')
data2 = pd.read_json('https://raw.githubusercontent.com/jonasweinschuetz/data_science_projekt/main/data/further_updated_german_canteens.json',encoding='utf8')
german_states_geo = pd.read_json('https://github.com/jonasweinschuetz/data_science_projekt/raw/main/data/deutschland_updated.geo.json', encoding='utf8')

data3 = data.join(data2.set_index('id'),on='mensa_id')
data3.drop(columns=data3.columns[0:2], axis=1, inplace=True)

state_frame_temp = data3.drop(columns = ['meal_id','meal_name','tags','date','name','city','address','coordinates','state'])
state_frame_temp = state_frame_temp.drop(columns = ['employee_price','guest_price'])
state_frame_temp = state_frame_temp.groupby(['vvo_status','state-id']).mean()
state_frame_temp = state_frame_temp.drop([-1,4])
state_frame_temp = state_frame_temp.round(2)
state_frame_temp = state_frame_temp.reset_index()

state_frame_vgn = state_frame_temp.loc[state_frame_temp['vvo_status']== 0]
state_frame_vgn = state_frame_vgn.drop(columns='vvo_status')
state_frame_veg = state_frame_temp.loc[state_frame_temp['vvo_status']== 1]
state_frame_veg = state_frame_veg.drop(columns='vvo_status')
state_frame_omni = state_frame_temp.loc[state_frame_temp['vvo_status']== 2]
state_frame_omni = state_frame_omni.drop(columns='vvo_status')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([


    dbc.Row([
            dbc.Col([
            dcc.Markdown('Heatmap of the Prices per categorie:',style={'textAlign':'center'})
        ],width = 12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.RadioItems(
                options=[
                    {"label": "Vegan Map", "value": 1},
                    {"label": "Vegetarian Map", "value": 2},
                    {"label": "Omnivor Map", "value": 3},
                ],
                value=1,
                inline=True,
                id="candidate",
            ),
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph")
            
        ])
    ])
])
@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value")
)

def display_choropleth(candidate):

        if candidate==1:
            temp = state_frame_vgn
        elif candidate==2:
            temp = state_frame_veg
        else:
            temp = state_frame_omni
        
        fig = px.choropleth_mapbox(temp,
                            locations='state-id',
                            geojson=german_states_geo,
                            color='student_price',
                            hover_name='student_price',
                            hover_data=['student_price'],    
                            mapbox_style='carto-positron',
                            center={'lat':51,'lon':10},
                            zoom=4
                            )
        return fig

if __name__ == "__main__":
    app.run_server(debug= True)

