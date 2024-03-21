import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json
from plotly.subplots import make_subplots

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

data = pd.read_csv("C:/Users/Micro/Desktop/git_projekte/git-hub/data_science_projekt/data/german-canteens(filtered).csv", sep="@",index_col=0)                    
geo_data = pd.read_json('C:/Users/Micro/Desktop/git_projekte/git-hub/data_science_projekt/data/further_updated_german_canteens.json',encoding='utf8')

data["date"] = pd.to_datetime(data["date"])
data.dropna(how="all", subset=['employee_price', 'student_price', "guest_price"], inplace=True)
student_prices = []
employee_prices = []

for index, entry in data.iterrows():
    guest_price = entry["guest_price"]
    student_price = entry["student_price"]
    employee_price = entry["employee_price"]
    
    student_prices.append(guest_price if pd.isna(student_price) else student_price)
    employee_prices.append(guest_price if pd.isna(employee_price) else employee_price)
    
data["student_price"] = student_prices
data["employee_price"] = employee_prices
data["weekday"] = data["date"].dt.day_name()

df = data
df["date"] = pd.to_datetime(df["date"])
df = df.drop(["meal_name", "meal_id", "tags", "vvo_status", ], axis=1)

df = df.join(geo_data.set_index('id'),on='mensa_id')
df = df.drop(["name", "address", "coordinates", "state-id", "city"], axis=1 )
states = list(df["state"].str.findall(".+"))
states = [state[0] for state in states]
states = set(states)
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

