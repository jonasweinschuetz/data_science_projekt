import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import re
import requests
import json

dash.register_page(__name__, path= '/', external_stylesheets =[dbc.themes.BOOTSTRAP])

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('# Feeding the Academic Appetite:',style={'textAlign':'center'})
        ],width = 12),
            dbc.Col([
            dcc.Markdown('### Price Dynamics and Dietary Trends of German Canteens',style={'textAlign':'center'})
        ],width = 12),
            dbc.Col([
            dcc.Markdown('**A Data Science Projekt from:**',style={'textAlign':'center'})
        ],width = 12),
            dbc.Col([
            dcc.Markdown('Iason Papandreou, Nikolaus Lieberum, Mika Friesenborg, Jonas Weinschütz',style={'textAlign':'center'})
        ],width = 12)
    ]),
        dbc.Row([dbc.Col([
            dcc.Markdown('**About This Project**',style={'textAlign':'center'})
            ],width = 12)
            ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

    This project aims to collect, analyze, and evaluate data from german educational canteens and cafeterias. 
    The project primarily focuses on prices and the distribution of vegan, vegetarian, and meat/omnivorous dishes 
    that are offered in the canteens.                     

    ''',style={'textAlign':'center'})   
        ])
    ]),
    ])
