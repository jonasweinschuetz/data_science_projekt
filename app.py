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
    "width": "13rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
nav = dbc.Nav([
     #dbc.NavItem(dbc.NavLink("Home", href=dash.page_registry['pages.home']['path'], active = "exact")),
     dbc.NavItem(dbc.NavLink("Home", href=dash.page_registry['pages.home']['path'], active = "exact")),
     dbc.NavItem(dbc.NavLink("How we collect the data", href=dash.page_registry['pages.collect']['path'], active = "exact")),
     dbc.NavItem(dbc.NavLink("How we clean the data", href=dash.page_registry['pages.cleaning']["path"], active = "exact")),            
     dbc.NavItem(dbc.NavLink("RQ 1", href=dash.page_registry['pages.rq1']["path"], active = "exact")),
     dbc.NavItem(dbc.NavLink("RQ 2", href=dash.page_registry['pages.rq2']["path"], active = "exact")),
     #dbc.NavItem(dbc.NavLink("RQ 3", href=dash.page_registry['pages.rq3']["path"], active = "exact")),
     #dbc.NavItem(dbc.NavLink("RQ 4", href=dash.page_registry['pages.rq4']["path"], active = "exact")),            
     #dbc.NavItem(dbc.NavLink("RQ 5", href=dash.page_registry['pages.rq5']["path"], active = "exact")),
     #dbc.NavItem(dbc.NavLink("RQ 6", href=dash.page_registry['pages.rq6']["path"], active = "exact")),            
     #dbc.NavItem(dbc.NavLink("RQ 7", href=dash.page_registry['pages.rq7']["path"], active = "exact")),
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
    app.run_server(debug=True)