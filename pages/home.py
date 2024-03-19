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
            dcc.Markdown('Hier könnte ihr home-text stehen',style={'textAlign':'center'})
        ],width = 12)
    ]),
    ])
