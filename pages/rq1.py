import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import datetime
import json
import os
dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

#os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')

file_path_data = "./data/"
df_monthly = pd.read_json(f'{file_path_data}avg_city_SH_monthly.json')
df = pd.read_csv(f'{file_path_data}meals_SH_canteens_merged_filtered_.csv', sep='@')


with open(f'{file_path_data}monthly_avg.json', 'r') as file:
    monthly_data = json.load(file)
    
df_monthly['date'] = pd.to_datetime(df_monthly['date'], unit='ms')
df_monthly_clean = df_monthly.dropna(subset=['average_price'])
cities = df_monthly_clean['city'].unique()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
color_idx = 0
fig1 = go.Figure()
city_trace_indices = {city: [] for city in cities}

for city in cities:
    city_data = df_monthly_clean[df_monthly_clean['city'] == city]
    if city_data.empty:
        continue
    X = city_data['date'].map(datetime.datetime.toordinal).values.reshape(-1, 1)
    y = city_data['average_price'].values

    # Linear regression
    reg = LinearRegression().fit(X, y)
    y_pred = reg.predict(X)

    # Plot data
    actual_trace = go.Scatter(x=city_data['date'], y=y, mode='markers+lines', name=city, marker_color=colors[color_idx])
    fig1.add_trace(actual_trace)
    city_trace_indices[city].append(len(fig1.data) - 1)

    # Plot trend line
    trend_trace = go.Scatter(x=city_data['date'], y=y_pred, mode='lines', name=f"{city} Trend", line=dict(color=colors[color_idx], dash='dash'))
    fig1.add_trace(trend_trace)
    city_trace_indices[city].append(len(fig1.data) - 1)

    color_idx = (color_idx + 1) % len(colors)

# buttons for dropdown
buttons = [
    dict(label='All',
         method='update',
         args=[{'visible': [True] * len(fig1.data)},
               {'title': 'Monthly Average Prices by City'}])
]

for city, indices in city_trace_indices.items():
    visible = [False] * len(fig1.data)
    for index in indices:
        visible[index] = True
    button = dict(label=city,
                  method='update',
                  args=[{'visible': visible},
                        {'title': f'Monthly Average Prices - {city}'}])
    buttons.append(button)

# Add dropdown
fig1.update_layout(
    updatemenus=[dict(buttons=buttons,
                      direction="down",
                      pad={"r": 10, "t": 10},
                      showactive=True,
                      x=0,
                      xanchor="left",
                      y=1.15,
                      yanchor="top")],
    title='Monthly Average Prices by City',
    xaxis_title='Date',
    yaxis_title='Average Price (in €)',
    legend=dict(title="City", orientation="v", x=1, xanchor="left", y=1, yanchor="auto")
)

# Prepare data
df['date'] = pd.to_datetime(df['date'])
df['student_price'] = pd.to_numeric(df['student_price'], errors='coerce')
df['employee_price'] = pd.to_numeric(df['employee_price'], errors='coerce')
df['guest_price'] = pd.to_numeric(df['guest_price'], errors='coerce')

# Calculate average prices by month
average_prices_by_month = df.groupby(df['date'].dt.to_period('M')).agg({
    'student_price': 'mean',
    'employee_price': 'mean',
    'guest_price': 'mean'
}).reset_index()

average_prices_by_month['date'] = average_prices_by_month['date'].dt.to_timestamp()

fig2 = go.Figure()
categories = ['student_price', 'employee_price', 'guest_price']
category_labels = ['Students', 'Employees', 'Guests']  # Translated
colors = ['blue', 'red', 'green']

for category, label, color in zip(categories, category_labels, colors):
    x = average_prices_by_month['date']
    y = average_prices_by_month[category]

    # Plot
    fig2.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name=label, marker_color=color))

    # Linear regression / trend line
    x_ordinal = np.array([i.toordinal() for i in x])
    x_ordinal = x_ordinal.reshape(-1, 1)  # Reshape for sklearn
    y_values = y.values.reshape(-1, 1)
    model = LinearRegression().fit(x_ordinal, y_values)

    # Plot
    y_pred = model.predict(x_ordinal)
    fig2.add_trace(go.Scatter(x=x, y=y_pred.flatten(), mode='lines', name=f'{label} Trend', line=dict(color=color, dash='dash')))

fig2.update_layout(title='Average Meal Prices in Schleswig-Holstein',
                  xaxis_title='Date',
                  yaxis_title='Average Price (€)',
                  legend_title="Category",
                  xaxis=dict(tickangle=-45))

# Make graph interactive
fig2.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True]},
                           {"title": "All Categories"}]),
                dict(label="Students",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False]},
                           {"title": "Average Prices for Students"}]),
                dict(label="Employees",
                     method="update",
                     args=[{"visible": [False, False, True, True, False, False]},
                           {"title": "Average Prices for Employees"}]),
                dict(label="Guests",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True]},
                           {"title": "Average Prices for Guests"}]),
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ]
)


# DataFrame
df_monthly = pd.DataFrame(monthly_data)
df_monthly['date'] = pd.to_datetime(df_monthly['date'], unit='ms')

colors = {'all': 'red', 'vegan': 'green', 'veget.': 'blue', 'meat': 'purple'}
fig3 = go.Figure()

trace_names = ['all', 'vegan', 'veget.', 'meat']
trace_visibility = {
    'All': [True] * 8,
    'Overall': [True, True] + [False] * 6,
    'Vegan': [False] * 2 + [True, True] + [False] * 4,
    'Veget.': [False] * 4 + [True, True] + [False] * 2,
    'Meat': [False] * 6 + [True, True],
}

for category in trace_names:
    display_name = 'overall' if category == 'all' else category

    fig3.add_trace(
        go.Scatter(x=df_monthly['date'], y=df_monthly[category], mode='markers+lines', name=display_name, marker_color=colors[category]),
    )

    # Linear regression
    df_non_null = df_monthly.dropna(subset=[category])
    X = np.array(range(len(df_non_null))).reshape(-1, 1)
    y = df_non_null[category].values.reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    trend_line = model.predict(np.array(range(len(df_monthly))).reshape(-1, 1))

    fig3.add_trace(
        go.Scatter(x=df_monthly['date'], y=trend_line.ravel(), mode='lines', name=f'{display_name} trend', line=dict(color=colors[category], dash='dot')),
    )

# Dropdown menu
buttons = []
for label, visibility in trace_visibility.items():
    button = dict(
        label=label,
        method="update",
        args=[{"visible": visibility},
              {"title": f"Monthly Average Prices by Category - {label}"}])
    buttons.append(button)

fig3.update_layout(
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0,
        xanchor="left",
        y=1.15,
        yanchor="top"
    )],
    title='Monthly Average Prices by Category',
    xaxis_title='Month',
    yaxis_title='Price',
    legend=dict(title="Category", orientation="v", x=1, xanchor="left", y=1, yanchor="auto")
)

## dash
layout = dbc.Container([
    dbc.Row([dbc.Col([
            dcc.Markdown('How does the average price for a meal change over the observed time frame (Schleswig-Holstein)?',style={'textAlign':'center'})
            ],width = 12)
            ]),
    
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph1", figure = fig1)
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph2", figure = fig2)  
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph3", figure = fig3)   
        ])
    ]),
])
