import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests
import json

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('# Data Cleaning',style={'textAlign':'center'})
        ],width = 12)
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

            The data cleaning process was relatively straightforward. To work with dish names and tags more effectively, we converted them to lowercase and filtered out line breaks and other special characters. The biggest issue we encountered was with prices. Unfortunately, there are canteens where one, two, or sometimes even all price tiers were missing. We suspect that this is due to some canteens, for example, having a single price for all their customers, which was then only recorded in the guest price line. We considered how to fill these gaps but ultimately decided not to consider missing prices for the respective price class calculation. 

            It is particularly unfortunate that in the OpenMensa database, there were no data entries for Berlin and Bremen, which is why these two states cannot be found in our price statistics. 

            The last point, which unfortunately came to our attention too late, is that in many canteens in Lower Saxony, almost 10 times as many dishes are found in the database on Fridays compared to the other weekdays. Unfortunately, we did not have the time to investigate potential causes of this phenomenon, but we had enough time to name it. Please keep the Lower Saxony Phenomenon in mind when reviewing weekday-specific data.

    ''',style={'textAlign':'center'})   
        ])
    ]),
 ])

