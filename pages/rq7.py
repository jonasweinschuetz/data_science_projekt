import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json


dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

# Extract coordinates
def extract_coordinate(coord, index):
    try:
        return coord[index]
    except TypeError:
        return None

# Load the data
#meals_df = pd.read_csv('./data/german-canteens(filtered).csv', sep='@', encoding='utf8')
meals_df = pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/german-canteens(filtered).csv', sep='@', encoding='utf8')
# Load geo data
with open('./data/further_updated_german_canteens.json', 'r', encoding='utf-8') as file:
    geo_data = json.load(file)
# Load your data
#csv_path = './data/german-canteens(filtered).csv'
csv_path = 'https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/german-canteens(filtered).csv'
df = pd.read_csv(csv_path, sep='@', encoding='utf8')
# Load JSON data and merge
json_path = './data/further_updated_german_canteens.json'
with open(json_path, 'r', encoding='utf-8') as file:
    state_info = json.load(file)

# Convert price columns to numeric, coercing errors
columns_to_convert = ['student_price', 'employee_price', 'guest_price']
for column in columns_to_convert:
    meals_df[column] = pd.to_numeric(meals_df[column], errors='coerce')

# Calculate the average price
meals_df['average_price'] = meals_df[columns_to_convert].mean(axis=1)

# Calculate the average price per mensa
avg_price_per_mensa = meals_df.groupby('mensa_id')['average_price'].mean().reset_index()

# Convert geo data to DataFrame and filter
geo_df = pd.DataFrame(geo_data)
geo_df_filtered = geo_df[geo_df['name'].str.contains("Mensa" or "mensa", case=False, na=False)]

# Merge the data
merged_data = pd.merge(avg_price_per_mensa, geo_df_filtered, left_on='mensa_id', right_on='id')

# Find the top 10 most expensive and most affordable mensas
top_10_expensive_mensas = merged_data.nlargest(100, 'average_price')
top_10_affordable_mensas = merged_data.nsmallest(100, 'average_price')

# Combine the data and mark each group
top_10_expensive_mensas['category'] = 'Expensive'
top_10_affordable_mensas['category'] = 'Affordable'
combined_data = pd.concat([top_10_expensive_mensas, top_10_affordable_mensas])

combined_data['latitude'] = combined_data['coordinates'].apply(lambda x: extract_coordinate(x, 0))
combined_data['longitude'] = combined_data['coordinates'].apply(lambda x: extract_coordinate(x, 1))
valid_coords = combined_data.dropna(subset=['latitude', 'longitude'])

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

state_df = pd.DataFrame(state_info)

# Merge on mensa_id to associate each mensa with its state
merged_df = pd.merge(df, state_df[['id', 'state']], left_on='mensa_id', right_on='id')

# Convert price columns to numeric, ensuring aggregation can be performed
price_columns = ['student_price', 'employee_price', 'guest_price']
for column in price_columns:
    merged_df[column] = pd.to_numeric(merged_df[column], errors='coerce')

# Drop rows with NaN values in any of the price columns to ensure clean data for aggregation
cleaned_df = merged_df.dropna(subset=price_columns)

# Group by state and calculate the mean for each price category
grouped = cleaned_df.groupby('state')[price_columns].mean().reset_index()

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
])
