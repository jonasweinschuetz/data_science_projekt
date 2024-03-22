import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
import os

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
#os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')

df = pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/data_webapp/rq4_df.csv',sep='@',encoding='utf8')

fig1 = px.histogram(df, 
                    x="weekday", 
                    y="student_price", 
                    marginal="violin", 
                    histfunc="avg", 
                    text_auto=True, 
                    title=f"Average meal price for each weekday in euro",
                    category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))
fig2 = px.histogram(df[df["mensa_id"] == 1216], 
                    x="weekday", 
                    y="student_price", 
                    marginal="violin", 
                    histfunc="avg", 
                    text_auto=True, 
                    title=f"Average meal price for Kiel, Mensa I per weekday in euro",
                    category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))

select = dbc.Select(
    options=[
        {"label": "Baden-Württemberg", "value": "Baden-Württemberg"},
        {"label": "Bayern", "value": "Bayern"},
        {"label": "Berlin", "value": "Berlin"},
        {"label": "Brandenburg", "value": "Brandenburg"},
        {"label": "Bremen", "value": "Bremen"},
        {"label": "Hamburg", "value": "Hamburg"},
        {"label": "Hessen", "value": "Hessen"},
        {"label": "Mecklenburg-Vorpommern", "value": "Mecklenburg-Vorpommern"},
        {"label": "Niedersachsen", "value": "Niedersachsen"},
        {"label": "Nordrhein-Westfalen", "value": "Nordrhein-Westfalen"},
        {"label": "Rheinland-Pfalz", "value": "Rheinland-Pfalz"},
        {"label": "Saarland", "value": "Saarland"},
        {"label": "Sachsen", "value": "Sachsen"},
        {"label": "Sachsen-Anhalt", "value": "Sachsen-Anhalt"},
        {"label": "Schleswig-Holstein", "value": "Schleswig-Holstein"},
        {"label": "Thüringen", "value": "Thüringen"},
    ],
    value="Schleswig-Holstein",
    id="selector3",
)

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('# 4. Does the day of the week influence average meal prices?',style={'textAlign':'center'})
        ],width = 12)
    ]),


    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            ## For this section we focused on the student prices.    
                        
            ### On the country scale:
                        
            At first glance, it is apparent that Friday, Saturday, and Sunday are by far the most affordable days of the week. As evidenced by the violin plot, Saturdays and Sundays are significantly underrepresented in the dataset, which likely renders the average prices for this days non-representative. Conversely, Fridays are overrepresented due to the Lower Saxony Phenomenon mentioned earlier, leading to the overrepresentation of prices in Lower Saxony for Friday and consequently pulling down the overall average. The price differences on the remaining weekdays are minimal and are most likely due to statistical noise :/

    ''',style={'textAlign':'center'})   
        ])
    ]),


    dbc.Row([
            dbc.Col([
            dcc.Graph(id="graph1",figure = fig1)
        ],width = 12)
    ]),
    dbc.Row([
            dbc.Col([
            dcc.Graph(id="graph2",figure = fig2)
        ],width = 12)
    ]),
    dbc.Row([
            dbc.Col([
            select
        ],width = 12)
    ]),
    
    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            ### On the state level: 

            Our next step was to look for patterns on a finer scale, so we generated the previous plot for each federal state. Saturdays and Sundays continue to be outliers. This is likely because they adhere to the average prices of canteens offering weekend dishes. Accordingly, these two days are sometimes more expensive and sometimes cheaper than weekdays.
            
            For the working week days we firstly tried to locate weekdays that differ at least 5% from the week mean. Only Lower Saxony had weekdays that met this criterium.  
            When glancing over the average weekday prices for each state there is no aperent strong trend visible. Some states have price jump of around 5 cents on Mondays or Fridays when compared to the weekly average, but this can be explained with statistical variance. One day that raised our interest was the Friday in Brandenburg. It is 15 cent more expensive compared to the work-week average in Brandenburg. In order to get a better idea for the data, we will show some handselected plots where the y-axis has been scaled in a way that highlights the otherwhise barely visible changes in price.


    ''',style={'textAlign':'center'})   
        ])
    ]),


    dbc.Row([
            dbc.Col([
            dcc.Graph(id="graph7")
        ],width = 12)
    ]),
      
])
@callback(
    Output("graph7", "figure"), 
    Input("selector3","value")   
)

def update_graph(value1):
    fig = px.histogram(df[df["state"] == value1], 
                       x="weekday", 
                       y="student_price", 
                       marginal="violin", 
                       histfunc="avg", 
                       text_auto=True, 
                       title="Average meal price each weekday in "+value1,
                       category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))
    return fig

