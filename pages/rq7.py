import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
#os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')

# fig wird erstellt

valid_coords = pd.read_csv('./data/data_webapp/rq7_valid_coords.csv',sep='@',encoding='utf8')
grouped = pd.read_csv('./data/data_webapp/rq7_grouped.csv',sep='@',encoding='utf8')

fig = px.scatter_geo(valid_coords,
                     lat='latitude',
                     lon='longitude',
                     hover_name='name',
                     # Removed the size parameter to make dots the same size
                     color='category',  # Differentiate between expensive and affordable
                     projection='mercator',
                     title='Top 100 Most Expensive and Affordable Mensas with "Mensa" in Name in Germany',
                     color_discrete_map={'Expensive': 'red', 'Affordable': 'green'}  # Set colors for categories, green for Affordable
                    )

# Here, you adjust the marker size directly in the layout of the figure.
fig.update_traces(marker=dict(size=10))  # Set a fixed size for all dots

fig.update_layout(mapbox_style="open-street-map", geo=dict(resolution=50))

fig.update_geos(fitbounds="locations", visible=True, countrycolor="Black",
                showcountries=True, countrywidth=0.5)


price_columns = ['student_price', 'employee_price', 'guest_price']

# Initialize the figure
fig2 = go.Figure()

# Add a trace for each price type, but only make the student_price trace visible initially
for price_type in price_columns:
    fig2.add_trace(
        go.Bar(
            x=grouped['state'], 
            y=grouped[price_type],
            name=price_type,
            visible= (price_type == 'student_price')  # Only the student_price is visible initially
        )
    )

# Create dropdown buttons for interactive change
buttons = []

for price_type in price_columns:
    buttons.append(
        dict(
            label=price_type,
            method="update",
            args=[{"visible": [price == price_type for price in price_columns]},
                  {"title": f"Average {price_type.replace('_', ' ').capitalize()} in German States"}]
        )
    )

# Add dropdown to the figure
fig2.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "active": 0,
    }],
    title="Average Student Price in German States",
    xaxis=dict(title="State"),
    yaxis=dict(title="Average Price (EUR)"),
    barmode="group"
)

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('Does the University’s location affect the average price of a dish?',style={'textAlign':'center'})
        ],width = 12)
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph12", figure = fig2)
            
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph13", figure = fig)
            
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

# Research Question 7: Does a university’s location influence the average price of meals for students?

## Impact of University Location on Student Meal Prices

Displayed in this graphic are the 100 most expensive and cheapest canteens in Germany. Notably, there is some overlap among these establishments. When accounting for the entire range, the cheapest canteens predominantly cluster in Lower Saxony and North Rhine-Westphalia, particularly along the border with the Netherlands. Surprisingly, numerous affordable university canteens are situated in the southern regions. Conversely, the most expensive canteens tend to be located in the south near the French border, with additional high-priced options in Schleswig-Holstein and throughout central Germany.


## Key Finding:

Significant disparities exist in student meal prices across different German states.

Interestingly, we observe no distinct east-west divide in the pricing patterns, contrary to prior expectations. While the southern German states tend to have slightly higher prices overall, it's noteworthy that some of the cheapest canteens also hail from the southern regions. This suggests a nuanced landscape where geographical location does not strictly dictate pricing.



''',style={'textAlign':'center'})   
        ])
    ]),
])
