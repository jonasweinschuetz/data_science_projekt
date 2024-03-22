import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
import os
import imageio as iio
dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
#os.chdir('C:/Users/Micro/Desktop/neues_repo/data_science_projekt')

bund_ki_res_frame= pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/data_webapp/rq2_bund_ki_res_frame.csv',sep='@',encoding='utf8')

bund_ki_res_frame.drop(columns=bund_ki_res_frame.columns[0], axis=1, inplace=True)

state_frame_temp = pd.read_csv('./data/data_webapp/rq2_state_frame_temp.csv',sep='@',encoding='utf8')
state_frame_temp.drop(columns=state_frame_temp.columns[0], axis=1, inplace=True)

file = open('./data/deutschland_updated.geo.json','r',encoding='utf8')
german_states_geo=json.load(file)
file.close()

#fig1 = fig = px.box(bund_ki_res_frame,color="variable", color_discrete_map={
#                 "ki_total": "rgb(144,12,63)",
#                 "ki_vgn": "rgb(144,12,63)",
#                  "ki_veg": "rgb(144,12,63)",
#                  "ki_omni": "rgb(144,12,63)",
#                  "ger_total": "DarkCyan",
#                  "ger_vgn": "DarkCyan",
#                  "ger_veg": "DarkCyan",
#                  "ger_omni": "DarkCyan",},
#                  )
# fig1.update_layout(xaxis_title='categories',yaxis_title='student_price (€)')

img = iio.imread("./data/data_webapp/boxplot_image.png")
img2 = px.imshow(img)




layout = dbc.Container([
    dbc.Row([dbc.Col([
            dcc.Markdown('# 2. How do average meal prices changes, compare with each other according to category (vegan/vegetarian/meat)?',style={'textAlign':'center'})
            ],width = 12)
    ]),
    dbc.Row([dbc.Col([
            dcc.Markdown(' ',style={'textAlign':'center'})
            ],width = 12)
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            To address the research question, we decided to classify the collected data into the categories Vegan/Vegetarian/Animal, then group them and juxtapose them. This resulted in the following figure:

    ''',style={'textAlign':'center'})   
        ])
    ]),



     dbc.Row([
         dbc.Col([
            dcc.Graph(id="graph1", figure = img2)
         ]),
     ]), 


    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            ## The graphic yields the following results:

            #### Price deviation from national average by meal category (left:mean, right: median)


    ''',style={'textAlign':'center'})   
        ])
    ]),



    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            | Location | Vegan | Vegetarian | Omnivorous | Vegan | Vegetarian | Omnivorous
            | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
            Germany: | -9.92 % | -2.89 % | +16.94 % | -4.76 % | 0.00 % | +11.90 % |

            From this table, it can be observed that a vegan dish is significantly more cost-effective compared to the values for the entire Germany, whereas a meat dish is significantly more expensive.
            We then repeated the same procedure for dishes from Kiel.
                        

            | Location | Vegan | Vegetarian | Omnivorous | Vegan | Vegetarian | Omnivorous
            | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
            Kiel: | -6.59 % | -7.74 % | +12.03 % | -14.71 % | -2.94 % | +17.65 % | 

            From this table, it can be inferred that Kiel reflects the nationwide trend.

            In general, it can be said that there are significant differences between the categories. While the price differences in vegetarian dishes are not quite as large (ranging between -2.89%/-7.74% (mean/median)) as in vegan/meat dishes.
            Particularly, noticeable differences can be observed within these categories, with variations of -9.92%/+16.94% (vegan/meat) (all states) and -6.59%/+12.03% (vegan/meat) (Kiel).

            We then further investigated how the price distribution within the categories varies among the federal states. This resulted in the following maps:
            

    ''',style={'textAlign':'left'})   
        ])
    ]),


    dbc.Row([
            dbc.Col([
            dcc.Markdown('## Heatmap of the Prices per categorie:',style={'textAlign':'center'})
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
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            ## Most expensive states (without Berlin, Bremen):
            - Vegan: Rhineland-Palatinate, Saarland, Schleswig-Holstein
            - Vegetarian: Rhineland-Palatinate, Hamburg, Saarland
            - Omnivorous: Rhineland-Palatinate, Hesse, Hamburg

            Generally, there is no significant difference between the "old" and "new" federal states. Also, we noticed that despite being often labeled as the most expensive university cafeteria city in Germany, 
            Sh only ranks in the top three in one of the three categories (vegan).


    ''',style={'textAlign':'left'})   
        ])
    ]),




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
          

