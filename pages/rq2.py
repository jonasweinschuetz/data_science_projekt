import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import os
dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
#os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')

bund_ki_res_frame= pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/data_webapp/rq2_bund_ki_res_frame.csv',sep='@',encoding='utf8')

bund_ki_res_frame.drop(columns=bund_ki_res_frame.columns[0], axis=1, inplace=True)

state_frame_temp = pd.read_csv('./data\data_webapp/rq2_state_frame_temp.csv',sep='@',encoding='utf8')
state_frame_temp.drop(columns=state_frame_temp.columns[0], axis=1, inplace=True)

file = open('./data/deutschland_updated.geo.json','r',encoding='utf8')
german_states_geo=json.load(file)
file.close()

fig1 = fig = px.box(bund_ki_res_frame,color="variable", color_discrete_map={
                "ki_total": "rgb(144,12,63)",
                "ki_vgn": "rgb(144,12,63)",
                "ki_veg": "rgb(144,12,63)",
                "ki_omni": "rgb(144,12,63)",
                "ger_total": "DarkCyan",
                "ger_vgn": "DarkCyan",
                "ger_veg": "DarkCyan",
                "ger_omni": "DarkCyan",},
                )
fig1.update_layout(xaxis_title='categories',yaxis_title='student_price (€)')

layout = dbc.Container([
    dbc.Row([dbc.Col([
            dcc.Markdown('How do average meal prices changes, compare with each other according to category (vegan/vegetarian/meat)?',style={'textAlign':'center'})
            ],width = 12)
    ]),
    dbc.Row([dbc.Col([
            dcc.Markdown('Price comparison of Kiel with the national average',style={'textAlign':'center'})
            ],width = 12)
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph1", figure = fig1)
        ]),
    ]), 
    dbc.Row([
            dbc.Col([
            dcc.Markdown('Heatmap of the Prices per categorie:',style={'textAlign':'center'})
        ],width = 12)
    ]),
    dbc.Row([
            dbc.Col(dbc.RadioItems(
                options=[
                    {"label": "student_price", "value": "student_price"},
                    {"label": "employee_price", "value": "employee_price"},
                    {"label": "guest_price", "value": "guest_price"},
                ],
                value="student_price",
                inline=True,
                id="selector1",
            ),
            ),
            dbc.Col(dbc.RadioItems(
                options=[
                    {"label": "Vegan Map", "value": 1},
                    {"label": "Vegetarian Map", "value": 2},
                    {"label": "Omnivor Map", "value": 3},
                ],
                value=1,
                inline=True,
                id="selector2",   
            ),
            ),
    ],),    
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph4")    
        ])
    ])
])
@callback(
    Output("graph4", "figure"), 
    Input("selector1","value"),
    Input("selector2", "value")   
)
def display_choropleth(selector1,selector2):
             
        if selector2==1:
            temp_vvo_status = 'vegan'
            temp_color_continuous_scale = 'mint'
            temp_title = 'price distribution for vegan dishes'
        elif selector2==2:
            temp_vvo_status = 'veget.'
            temp_color_continuous_scale = 'PuBu'
            temp_title = 'price distribution for vegetarian dishes'
        else:
            temp_vvo_status = 'meat'
            temp_color_continuous_scale = 'burg'
            temp_title = 'price distribution for dishes containing animal ingredients' 
            
        range_color = (0,state_frame_temp['average '+ selector1].max())
        
        fig2 = px.choropleth_mapbox(state_frame_temp.loc[state_frame_temp['vvo_status']== temp_vvo_status,['state-id','average ' + selector1]],
                            locations='state-id',
                            geojson=german_states_geo,
                            color='average '+selector1,
                            color_continuous_scale=temp_color_continuous_scale,
                            hover_name='average ' + selector1,
                            hover_data=['average ' + selector1],     
                            mapbox_style='carto-positron',
                            center={'lat':51,'lon':10},
                            zoom=3.5,
                            title = temp_title
                            )        
        return fig2
          

