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
            dcc.Markdown('# 1. How has the average price for a meal in Schleswig-Holstein changed since 2021?',style={'textAlign':'center'})
            ],width = 12)
            ]),
    

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

    ## Exploring Meal Price Changes in Schleswig-Holstein Since 2021

    To investigate the question of how meal prices of canteens have evolved in Schleswig-Holstein since 2021, we compiled a dataset from all canteens in the region. This dataset, which dates back to 2021, combines information from the OpenMensa API with data obtained through web scraping (see Data Collection). Over this period, the dynamics of meal pricing within Schleswig-Holstein\'s canteens have experienced noticeable shifts. In our analysis, we consider various factors: geographical (by city), status-based (student, employee, guest), and dietary categories (vegan, vegetarian, omnivorous). We aim to unravel the intricacies of these pricing adjustments.

    ### Impact of Location on Price Change

    Analysis of the average canteen meal pricing data across cities reveals that each city within Schleswig-Holstein has experienced significant price changes. Kiel, Flensburg, and Heide have seen a steady rise in meal prices. Lübeck, meanwhile, exhibits the smallest increase in prices in EUR terms, with only a marginally smaller percentage increase compared to the other cities. This suggests that, in general, local pricing in Lübeck has been more affordable.                      

    ''',style={'textAlign':'center'})   
        ])
    ]),


    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph1", figure = fig1)
        ])
    ]),

    
    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

    **Average Price Change (Per Year Since 2021)**

    | Location             | Price Increase (€/Year) | Percentage Increase (%/Year) |
    |----------------------|-------------------------|-------------------------------|
    | Kiel:                | 0.41 €                  | 10.41 %                      |
    | Flensburg:           | 0.42 €                  | 11.05 %                      |
    | Lübeck:              | 0.16 €                  | 8.67 %                       |
    | Heide:               | 0.47 €                  | 9.36 %                       |
    | **Schleswig-Holstein:** | 0.36 €              | 9.87 %                       |

    In 2022 and 2023, canteen meal prices in Schleswig-Holstein (SH) rose noticeably, yet remained below the national food inflation rate. Despite the significant differences observed between cities across these years, an overarching trend of increasing prices is evident.
    
    ''',style={'textAlign':'center'})   
        ])
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''


    **Annual Price Changes (2022 and 2023)**
                        
    | Location          | 2022   | 2023  |
    |-------------------|-------|-------|
    | Kiel:             | 8.7 %  | 12.4 % |
    | Flensburg:        | 1.7 %  | 9.8 %  |
    | Lübeck:           | 15.8 % | 6.8 %  |
    | Heide:            | 11.8 % | 12.2 % |
    | **SH:**           | 9.5 %  | 10.3 % |
    | **Food Inflation:** | 13.4 % | 12.4 % |

    _Food Inflation = Germany-wide food inflation rate ([destatis.de](https://destatis.de))_

    ## Impact of Visitor Status on Price Change

    An in-depth examination of meal price changes in canteens based on visitor status (student, employee, guest) reveals differentiated impacts. Guests experienced an annual increase of 10.92 % (0.47 €), employees saw a 10.47 % rise (0.42 €), and students encountered the steepest increase at 10.94 % (0.31 €). This tiered pricing model demonstrates the canteens attempts to maintain affordability amidst inflation, tailored for students, employees, and guests.

    ''',style={'textAlign':'center'})   
        ])
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph2", figure = fig2)  
        ])
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

    ## Impact of Dietary Categories on Price Change

    Further analysis delves into price variations across dietary categories: vegan, vegetarian, and meat-based meals. Surprisingly, vegan meals underwent the highest price adjustments, followed by meat-based and then vegetarian options. Specifically, vegan dishes experienced an average annual price increase of 18.33 % (0.54 €), with meat-based (16.84 %, 0.67 €) and vegetarian (15.41 %, 0.48 €) meals seeing more modest rises. The graph below illustrates the substantial price volatility of vegan meals compared to meat-based options, potentially reflecting the increasing costs of vegan food production and a growing demand for plant-based diets among students.
        
    ''',style={'textAlign':'center'})   
        ])
    ]),


    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph3", figure = fig3)   
        ])
    ]),
    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

    ## Conclusion

    Our comprehensive analysis of meal price changes in Schleswig-Holstein\'s canteens since 2021 highlights several key trends. Geographical location, visitor status, and dietary choices significantly influence price adjustments, with vegan meals experiencing the highest increases. Despite the inflationary pressures, canteen meal prices in the region have generally remained below the national food inflation rate, suggesting efforts by canteen operators to keep meals accessible to their primary clientele. As dietary habits continue to evolve and economic conditions change, these trends offer valuable insights for diverse and economically sensitive people such as students, employees, and guests in educational institutions.


    ''',style={'textAlign':'center'})   
            ])
        ]),
])

