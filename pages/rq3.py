import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json


dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

 

#df = pd.read_csv('./data/german-canteens(filtered).csv', sep='@', engine='python')
df =pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/german-canteens(filtered).csv','r',encoding='utf8')
# Load your data
#data = pd.read_csv('./data/german-canteens(filtered).csv', sep='@', encoding='utf8')
data =pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/german-canteens(filtered).csv','r',encoding='utf8')    

data2 = pd.read_json('./data/further_updated_german_canteens.json', encoding='utf8')

with open('./data/deutschland_updated.geo.json', 'r', encoding='utf8') as file:
    german_states_geo = json.load(file)

data3 = data.join(data2.set_index('id'), on='mensa_id')
data3.drop(columns=data3.columns[0:2], axis=1, inplace=True)

# Convert 'date' column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Convert price columns to numeric type, coercing errors to NaN
df['student_price'] = pd.to_numeric(df['student_price'], errors='coerce')
df['employee_price'] = pd.to_numeric(df['employee_price'], errors='coerce')
df['guest_price'] = pd.to_numeric(df['guest_price'], errors='coerce')

# Function to remove outliers based on the IQR for bi-weekly averages
def remove_outliers_bi_weekly(df):
    columns = ['student_price', 'employee_price', 'guest_price']
    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[column] >= (Q1 - 1.5 * IQR)) & (df[column] <= (Q3 + 1.5 * IQR))]
    return df

# Drop rows with NaN or zero values in any of the price columns
df_cleaned = df.dropna(subset=['student_price', 'employee_price', 'guest_price'])
df_cleaned = df_cleaned[(df_cleaned['student_price'] > 0) &
                        (df_cleaned['employee_price'] > 0) &
                        (df_cleaned['guest_price'] > 0)]

# Resample and calculate bi-weekly (2-week) averages
bi_weekly_averages = df_cleaned.set_index('date').resample('2W')['student_price', 'employee_price', 'guest_price'].mean().reset_index()

# Remove outliers based on the IQR for bi-weekly averages
bi_weekly_averages_no_outliers = remove_outliers_bi_weekly(bi_weekly_averages)

# Plot using Plotly
fig = go.Figure()

# Add traces for student, employee, and guest prices
fig.add_trace(go.Scatter(x=bi_weekly_averages_no_outliers['date'], y=bi_weekly_averages_no_outliers['student_price'], mode='lines+markers', name='Average Student Price'))
fig.add_trace(go.Scatter(x=bi_weekly_averages_no_outliers['date'], y=bi_weekly_averages_no_outliers['employee_price'], mode='lines+markers', name='Average Employee Price'))
fig.add_trace(go.Scatter(x=bi_weekly_averages_no_outliers['date'], y=bi_weekly_averages_no_outliers['guest_price'], mode='lines+markers', name='Average Guest Price'))

# Add dotted trend lines
# Student Price Trend
fig.add_trace(go.Scatter(x=[bi_weekly_averages_no_outliers['date'].iloc[0], bi_weekly_averages_no_outliers['date'].iloc[-1]], 
                         y=[bi_weekly_averages_no_outliers['student_price'].iloc[0], bi_weekly_averages_no_outliers['student_price'].iloc[-1]], 
                         mode='lines', line=dict(dash='dot'), name='Trend - Student'))

# Employee Price Trend
fig.add_trace(go.Scatter(x=[bi_weekly_averages_no_outliers['date'].iloc[0], bi_weekly_averages_no_outliers['date'].iloc[-1]], 
                         y=[bi_weekly_averages_no_outliers['employee_price'].iloc[0], bi_weekly_averages_no_outliers['employee_price'].iloc[-1]], 
                         mode='lines', line=dict(dash='dot'), name='Trend - Employee'))

# Guest Price Trend
fig.add_trace(go.Scatter(x=[bi_weekly_averages_no_outliers['date'].iloc[0], bi_weekly_averages_no_outliers['date'].iloc[-1]], 
                         y=[bi_weekly_averages_no_outliers['guest_price'].iloc[0], bi_weekly_averages_no_outliers['guest_price'].iloc[-1]], 
                         mode='lines', line=dict(dash='dot'), name='Trend - Guest'))

fig.update_layout(title='Bi-Weekly Average Meal Prices in German Canteens Over Time (Outliers Removed)',
                  xaxis_title='Date',
                  yaxis_title='Price (EUR)',
                  legend_title='Category')

# Ensure you're calculating the min/max after merging to avoid NaN issues
data3['student_price'] = pd.to_numeric(data3['student_price'], errors='coerce')
data3['employee_price'] = pd.to_numeric(data3['employee_price'], errors='coerce')
data3['guest_price'] = pd.to_numeric(data3['guest_price'], errors='coerce')

# Recalculate min and max after conversion to numeric, setting max to 10 for all
range_color_student = (data3['student_price'].min(), min(data3['student_price'].max(), 10))
range_color_employee = (data3['employee_price'].min(), min(data3['employee_price'].max(), 10))
range_color_guest = (data3['guest_price'].min(), min(data3['guest_price'].max(), 10))

fig2 = go.Figure()

# Adjust colorscale if needed to ensure visibility of variations
colorscale = "Viridis"

# Adding traces for each category with zmax set to 10
fig2.add_trace(go.Choroplethmapbox(
    geojson=german_states_geo,
    locations=data3['state-id'],
    z=data3['student_price'],
    colorscale=colorscale,
    zmin=range_color_student[0],
    zmax=10,  # Updated zmax to 10
    name='Student Prices',
    
    visible=True
))

fig2.add_trace(go.Choroplethmapbox(
    geojson=german_states_geo,
    locations=data3['state-id'],
    z=data3['employee_price'],
    colorscale=colorscale,
    zmin=range_color_employee[0],
    zmax=10,  # Updated zmax to 10
    name='Employee Prices',
    
    visible=False
))

fig2.add_trace(go.Choroplethmapbox(
    geojson=german_states_geo,
    locations=data3['state-id'],
    z=data3['guest_price'],
    colorscale=colorscale,
    zmin=range_color_guest[0],
    zmax=10,  # Updated zmax to 10
    name='Guest Prices',
    
    visible=False
))

# Update layout
fig2.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3.5,
    mapbox_center={"lat": 51, "lon": 10},
    title='Price Distribution in German Canteens',
    updatemenus=[{
        'buttons': [
            {'label': 'Student Prices', 'method': 'update', 'args': [{'visible': [True, False, False]}]},
            {'label': 'Employee Prices', 'method': 'update', 'args': [{'visible': [False, True, False]}]},
            {'label': 'Guest Prices', 'method': 'update', 'args': [{'visible': [False, False, True]}]}
        ],
        'direction': 'down',
        'showactive': True,
    }]
)

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('How is the relation between prizes of different customer status (student/faculty/guests)?',style={'textAlign':'center'})
        ],width = 12)
    ]),
    
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph5", figure = fig2 )
            
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph6", figure = fig)           
        ])
    ]),    
])




