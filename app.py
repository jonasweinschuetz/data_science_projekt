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
     dbc.NavItem(dbc.NavLink("How we collect the data", href=dash.page_registry['pages.collect']['path'], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("How we clean the data", href=dash.page_registry['pages.cleaning']["path"], active = "exact", style = LETTER_STYLE)),            
     dbc.NavItem(dbc.NavLink("How does the average price for a mealchange over the observed time frame (Schleswig-Holstein)?", href=dash.page_registry['pages.rq1']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("How do average meal prices changes, compare with each other according to category (vegan/vegetarian/meat)?", href=dash.page_registry['pages.rq2']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("How is the relation between prizesof different customer status (student/faculty/guests)?", href=dash.page_registry['pages.rq3']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("Do weekdays affect the average meal prices?", href=dash.page_registry['pages.rq4']["path"], active = "exact", style = LETTER_STYLE)),            
     dbc.NavItem(dbc.NavLink("Do weekdays affect the variety of meal categories?", href=dash.page_registry['pages.rq5']["path"], active = "exact", style = LETTER_STYLE)),
     dbc.NavItem(dbc.NavLink("What are the most common dishes/per state?", href=dash.page_registry['pages.rq6']["path"], active = "exact", style = LETTER_STYLE)),            
     dbc.NavItem(dbc.NavLink("Does the University’s location affect the average price of a dish? ", href=dash.page_registry['pages.rq7']["path"], active = "exact", style = LETTER_STYLE)),
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