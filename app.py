import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "15rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

LETTER_STYLE ={"font-size": 14}

nav = dbc.Nav([
     dbc.NavItem(dbc.NavLink("Home", href=dash.page_registry['pages.home']['path'], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("Data collection", href=dash.page_registry['pages.collect']['path'], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("Data cleaning", href=dash.page_registry['pages.cleaning']["path"], active = "exact", style = LETTER_STYLE)),            
     dbc.NavItem(dbc.NavLink("How has the average price for a meal in Schleswig-Holstein changed since 2021??", href=dash.page_registry['pages.rq1']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("How do average student meal prices compare according to their category?", href=dash.page_registry['pages.rq2']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("How does the average price change for visitors in Germany since 2023?", href=dash.page_registry['pages.rq3']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("Does the day of the week influence average meal prices?", href=dash.page_registry['pages.rq4']["path"], active = "exact", style = LETTER_STYLE)),            
     dbc.NavItem(dbc.NavLink("Does the weekday influence the availability of dietary options in German canteens?", href=dash.page_registry['pages.rq5']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("What are the most frequent words in meal names by category and geographic location?", href=dash.page_registry['pages.rq6']["path"], active = "exact", style = LETTER_STYLE)),            
     dbc.NavItem(dbc.NavLink("Does a university’s location influence the average price of meals for students?", href=dash.page_registry['pages.rq7']["path"], active = "exact", style = LETTER_STYLE)),
    ], 
    vertical = True,
    pills=True,
    style=SIDEBAR_STYLE,
    )


app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([nav,],
                    width = 1),
            dbc.Col([dash.page_container,])
        ])
    ],
    className="dbc",
    
)

if __name__ == "__main__":
    app.run_server(debug=False)
