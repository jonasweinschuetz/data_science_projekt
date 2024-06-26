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
 
bi_weekly_averages_no_outliers = pd.read_csv('./data/data_webapp/rq3_bi_weekly_averages_no_outliers.csv',sep='@',encoding='utf8')

#data3 = pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/data_webapp/rq3_data3.csv',sep='@',encoding='utf8')

avg_student_prices = pd.read_csv('./data/data_webapp/rq3_avg_student_prices.csv', sep='@', encoding='utf8')
avg_employee_prices = pd.read_csv('./data/data_webapp/rq3_avg_employee_prices.csv', sep='@', encoding='utf8')
avg_guest_prices = pd.read_csv('./data/data_webapp/rq3_avg_guest_prices.csv', sep='@', encoding='utf8')


with open('./data/deutschland_updated.geo.json', 'r', encoding='utf8') as file:
    german_states_geo = json.load(file)

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




# Recalculate min and max after conversion to numeric, setting max to 10 for all
range_color_student = (avg_student_prices['student_price'].min(), min(avg_student_prices['student_price'].max(), 7))
range_color_employee = (avg_employee_prices['employee_price'].min(), min(avg_employee_prices['employee_price'].max(), 7))
range_color_guest = (avg_guest_prices['guest_price'].min(), min(avg_guest_prices['guest_price'].max(), 7))


# wird erstell


fig2 = go.Figure()

# Adjust colorscale if needed to ensure visibility of variations
colorscale = "Viridis"

# Adding traces for each category with zmax set to 10
fig2.add_trace(go.Choroplethmapbox(
    geojson=german_states_geo,
    locations=avg_student_prices['state-id'],
    z=avg_student_prices['student_price'],
    colorscale=colorscale,
    zmin=range_color_student[0],
    zmax=5,  
    name='Average Student Prices',
    visible=True
))

fig2.add_trace(go.Choroplethmapbox(
    geojson=german_states_geo,
    locations=avg_employee_prices['state-id'],
    z=avg_employee_prices['employee_price'],
    colorscale=colorscale,
    zmin=range_color_employee[0],
    zmax=7,  
    name='Average Employee Prices',
    visible=False
))

fig2.add_trace(go.Choroplethmapbox(
    geojson=german_states_geo,
    locations=avg_guest_prices['state-id'],
    z=avg_guest_prices['guest_price'],
    colorscale=colorscale,
    zmin=range_color_guest[0],
    zmax=10,  
    name='Average Guest Prices',
    visible=False
))

# Update layout
fig2.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3.5,
    mapbox_center={"lat": 51, "lon": 10},
    title='Average Price Distribution in German Canteens',
    updatemenus=[{
        'buttons': [
            {'label': 'Average Student Prices', 'method': 'update', 'args': [{'visible': [True, False, False]}]},
            {'label': 'Average Employee Prices', 'method': 'update', 'args': [{'visible': [False, True, False]}]},
            {'label': 'Average Guest Prices', 'method': 'update', 'args': [{'visible': [False, False, True]}]}
        ],
        'direction': 'down',
        'showactive': True,
    }]
)

layout = dbc.Container([
    dbc.Row([dbc.Col([
            dcc.Markdown('# 3. How does the average price change for visitors in Germany since 2023?',style={'textAlign':'center'})
            ],width = 12)
            ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''


    ## How has the average price for a meal in Germany changed since 2023? 

    ### Exploring Meal Price Changes in Germany Since 2023

    To explore this research question we build a data set for all canteens in Germany. This data set dates back to 1.1.2023 and is from the OpenMensa API. Since 2023, the dynamics of meal pricing within Germanys canteens have undergone some changes.


    ''',style={'textAlign':'center'})   
        ])
    ]),
    

    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph6", figure = fig )       
        ])
    ]),

    dbc.Row([
        dbc.Col([
           dcc.Markdown('''
         
    ## Average Data
    This table illustrates the absolute price changes for different price categories. The 'Student Price' experienced a modest increase of 0.13 € since 2023, while the 'Employee Price' saw a slightly larger increase of 0.19 € during the same period. Notably, the 'Guest Price' exhibited the highest absolute change, rising by 0.33 €. 

    | Price Category   | Absolute Price Change |
    |------------------|-----------------------|
    | Student Price    | 0.13 €                |
    | Employee Price   | 0.19 €                |
    | Guest Price      | 0.33 €                |

    ## Trend Data                  
    This table showcases the percentage changes in prices across different categories. The 'Student Price' witnessed a modest increase of 5.60%, reflecting moderate inflationary pressures since 2023. In comparison, the 'Employee Price' saw a slightly higher percentage rise of 6.30%, indicating a marginally greater impact on this category. Remarkably, the 'Guest Price' experienced the most significant percentage change, soaring by 9.30%.                        

    | Price Category   | Percentage Change |
    |------------------|-------------------|
    | Student Price    | 5.60 %            |
    | Employee Price   | 6.30 %            |
    | Guest Price      | 9.30 %            |

    ## Combined Data

    | **Average price change since 2023 (absolute)** |      |
    |-----------------------------------------------|------|
    | **Student Price:**                            | 0.13 €, or 5.60 %  |
    | **Employee Price:**                           | 0.19 €, or 6.30 %  |
    | **Guest Price:**                              | 0.33 €, or 9.30 %  |
                            

    ''',style={'textAlign':'center'})   
            ])
        ]),
                
    dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph5", figure = fig2)           
        ])
    ]),

])




