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
            dcc.Markdown('# Data Collection',style={'textAlign':'center'})
        ],width = 12)
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''
                        
        ## Web Scraping:

        The web-scraped dataset was obtained from one of our classmates, [Lia Lenckowski](https://github.com/llenck) Her web scraper queries the subpages of the Studentenwerk SH responsible for the meal plan of each university. Each of these subpages can be passed an argument representing one of the canteens that the university has. Then, only the container containing the meal table needs to be extracted from the received HTML, and the dishes are loaded into a JSON-lines file. Since the canteens always provide their weekly schedule, a request is made for each canteen of each university of the Studentenwerk once a week.

        ## OpenMensa API:

        To build our dataset from the OpenMensa API, we first acquired a dataset containing all canteen locations and IDs (in total 1210) using its API, then mapped these to German cities and states using a dictionary created from scraping [Wikipedia's page of German cities](https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_in_Deutschland). This allowed us to filter down to 687 canteens within Germany. Tackling the challenge of long request times and limited data retrieval (one day's meals per canteen ID per call), we automated the data collection process, running it continuously in multiple parallel processes on five Raspberry Pis. Specifically, we focused on collecting meal data from 2023 onwards for all German canteens and build a dedicated dataset for Schleswig-Holstein (SH) canteens starting from 2021 - the earliest data available for SH. Ultimately, we created three comprehensive datasets: one detailing Schleswig-Holstein canteens since 2021, a nationwide dataset from 2023, and a mapping of all German OpenMensa canteens with their respective locations (geo data) and IDs.

    ''',style={'textAlign':'center'})  


        ])
    ]),

])