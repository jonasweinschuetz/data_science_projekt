import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import base64

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

LETTER_STYLE ={"font-size": 14}

logo_path = "./data/Logo.png"
encoded_image = base64.b64encode(open(logo_path, 'rb').read()).decode()

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(html.Img(src=f'data:image/png;base64,{encoded_image}', height="30px"), width="auto"),
                dbc.Col(dbc.NavbarBrand(" ", className="ms-2"), align="center", width="auto"),
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Home", href=dash.page_registry['pages.home']['path'])),
                            dbc.NavItem(dbc.NavLink("Data Collection", href=dash.page_registry['pages.collect']['path'])),
                            dbc.NavItem(dbc.NavLink("Data Cleaning", href=dash.page_registry['pages.cleaning']['path'])),
                            dbc.DropdownMenu(
                                children=[
                                    dbc.DropdownMenuItem("How has the average price for a meal in Schleswig-Holstein changed since 2021?", href=dash.page_registry['pages.rq1']['path']),
                                    dbc.DropdownMenuItem("How do average student meal prices compare according to their category?", href=dash.page_registry['pages.rq2']['path']),
                                    dbc.DropdownMenuItem("How does the average price change for visitors in Germany since 2023?", href=dash.page_registry['pages.rq3']['path']),
                                    dbc.DropdownMenuItem("Does the day of the week influence average meal prices?", href=dash.page_registry['pages.rq4']['path']),
                                    dbc.DropdownMenuItem("Does the weekday influence the availability of dietary options in German canteens?", href=dash.page_registry['pages.rq5']['path']),
                                    dbc.DropdownMenuItem("What are the most frequent words in meal names by category and geographic location?", href=dash.page_registry['pages.rq6']['path']),
                                    dbc.DropdownMenuItem("Does a university’s location influence the average price of meals for students?", href=dash.page_registry['pages.rq7']['path']),
                                ],
                                nav=True,
                                in_navbar=True,
                                label="Research Questions",
                            ),
                        ],
                        className="ms-auto",  # This class aligns the nav items to the right
                        navbar=True,
                    ),
                    width="auto",
                ),
            ],
            align="center",
        ),
    ]),
    color="primary",
    dark=True,
    className="mb-5",  # Adds space below the navbar
)

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row([
            dbc.Col([dash.page_container], width=12)
        ])
    ],
    className="dbc",
)

if __name__ == "__main__":
    app.run_server(debug=False)
