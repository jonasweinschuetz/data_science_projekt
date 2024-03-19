import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import re
import requests
import json

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

data = pd.read_csv('C:/Users/Micro/Desktop/git_projekte/git-hub/data_science_projekt/data/german-canteens(filtered).csv',sep='@', encoding='utf8')
data2 = pd.read_json('C:/Users/Micro/Desktop/git_projekte/git-hub/data_science_projekt/data/further_updated_german_canteens.json',encoding='utf8')

file = open('C:/Users/Micro/Desktop/git_projekte/git-hub/data_science_projekt/data/deutschland_updated.geo.json','r',encoding='utf8')
german_states_geo=json.load(file)
file.close()

#url_german_states_geo = 'C:/Users/Micro/Desktop/git_projekte/git-hub/data_science_projekt/data/deutschland_updated.geo.json'
#resp = requests.get(url_german_states_geo)
#german_states_geo = json.loads(resp.text)
#german_states_geo = json.load(url_german_states_geo)
data3 = data.join(data2.set_index('id'),on='mensa_id')
data3.drop(columns=data3.columns[0:2], axis=1, inplace=True)

ki_ges_t=data3.loc[data3['city'] == 'Kiel']
ki_ges_t = ki_ges_t.drop(columns = ['date','meal_id','meal_name','tags','date','name','address','coordinates','state','state-id','city','employee_price','guest_price'])
ki_vgn_t = ki_ges_t.loc[ki_ges_t['vvo_status'] == 'vegan'].rename(columns={"student_price": "ki_vgn"})
ki_veg_t = ki_ges_t.loc[ki_ges_t['vvo_status'] == 'veget.'].rename(columns={"student_price": "ki_veg"})
ki_omn_t = ki_ges_t.loc[ki_ges_t['vvo_status'] == 'meat'].rename(columns={"student_price": "ki_omni"})
ki_ges_t = ki_ges_t.rename(columns={"student_price": "ki_gesammt"})

ges_t = data.drop(columns = ['Unnamed: 0','mensa_id','date','meal_id','meal_name','tags','employee_price','guest_price'])

vgn_t = ges_t.loc[ges_t['vvo_status'] == 'vegan'].rename(columns={"student_price": "Gesammt_vgn"})
veg_t = ges_t.loc[ges_t['vvo_status'] == 'veget.'].rename(columns={"student_price": "Gesammt_veg"})
omn_t = ges_t.loc[ges_t['vvo_status'] == 'meat'].rename(columns={"student_price": "Gesammt_omni"})
ges_t = ges_t.rename(columns={"student_price": "Gesammt"})
bund_ki_res_frame = pd.concat([ges_t,vgn_t,veg_t,omn_t,ki_ges_t,ki_vgn_t,ki_veg_t,ki_omn_t],axis=1)
bund_ki_res_frame = bund_ki_res_frame.drop(columns = ['vvo_status'])
bund_ki_res_frame.loc[bund_ki_res_frame['Gesammt_vgn'] == 99.99, 'Gesammt_vgn']= pd.NA
bund_ki_res_frame.loc[bund_ki_res_frame['Gesammt'] == 99.99, 'Gesammt']= pd.NA

state_frame_temp = data3.drop(columns = ['meal_id','meal_name','tags','date','name','city','address','coordinates','state'])        
state_frame_temp = state_frame_temp.groupby(['vvo_status','state-id']).mean()
state_frame_temp = state_frame_temp.drop('-1')
state_frame_temp = state_frame_temp.round(2)
state_frame_temp = state_frame_temp.reset_index()   
state_frame_temp = state_frame_temp.rename(columns={"student_price": "average student_price"})
state_frame_temp = state_frame_temp.rename(columns={"employee_price": "average employee_price"})
state_frame_temp = state_frame_temp.rename(columns={"guest_price": "average guest_price"})

fig1 = fig = px.box(bund_ki_res_frame,color="variable", color_discrete_map={
                "ki_gesammt": "rgb(144,12,63)",
                "ki_vgn": "rgb(144,12,63)",
                "ki_veg": "rgb(144,12,63)",
                "ki_omni": "rgb(144,12,63)",
                "Gesammt": "DarkCyan",
                "Gesammt_vgn": "DarkCyan",
                "Gesammt_veg": "DarkCyan",
                "Gesammt_omni": "DarkCyan",},)

layout = dbc.Container([
    dbc.Row([dbc.Col([
            dcc.Markdown('Vergleich Kiel mit Bundesdurchschnitt',style={'textAlign':'center'})
            ],width = 12)
            ]),
    
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph1",
                     figure = fig1)
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
           dcc.Graph(id="graph2")
            
        ])
    ])
])
@callback(
    Output("graph2", "figure"), 
    Input("selector1","value"),
    Input("selector2", "value")
    
)

def display_choropleth(selector1,selector2):
        
          
        if selector2==1:
            temp_vvo_status = 'vegan'
            temp_color_continuous_scale = 'mint'
            temp_title = 'Preisverteilung für vegane Gerichte nach ' + selector1
        elif selector2==2:
            temp_vvo_status = 'veget.'
            temp_color_continuous_scale = 'PuBu'
            temp_title = 'Preisverteilung für vegetarische Gerichte nach ' + selector1
        else:
            temp_vvo_status = 'meat'
            temp_color_continuous_scale = 'burg'
            temp_title = 'Preisverteilung für Gerichte mit tierischen Inhaltsstoffen nach ' + selector1
            
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
          

