import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
import os

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')

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
            dcc.Markdown('Do weekdays affect the average meal prices?',style={'textAlign':'center'})
        ],width = 12)
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

