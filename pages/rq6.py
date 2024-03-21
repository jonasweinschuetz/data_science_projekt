import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
from wordcloud import WordCloud, STOPWORDS
import os

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
#os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')

df = pd.read_csv('https://media.githubusercontent.com/media/jonasweinschuetz/data_science_projekt/main/data/data_webapp/rq6_df.csv',sep='@',encoding='utf8')

uninteressant = ['und','von','Der','das','mit','bestellzeit','abgelaufen','gemüse','dazu', "glw", "glg", "mi", "ei", 
                 "je 100g", "g", "portion", "abgelaufen", "sl", "ein", "sf", "gld", "euch", "uns", "freuen","wir","auf","tagesgericht","gibt"]
STOPWORDS.update(uninteressant)

def name_wordcloud(df, full_names=False, category="", state="", w=4000, h=1800):
    # filter after category and state if necessary
    
    if category:
        df = df[df["vvo_status"] == category]
    
    if state:
        df = df[df["state"] == state]
    
    if full_names:
        # get the number of appearances of every dish name
        df = df.groupby(["meal_name"]).count()
        # mensa_id should never be a nan, so it is a reliable feature for the total name count   
        df = df["mensa_id"]
        # turn to dictionary and create 
        dictionary = df.to_dict() 
        wordcloud = WordCloud(background_color='white', 
                              width=w, 
                              height=h, 
                              relative_scaling=0.4, 
                              colormap="Dark2",).generate_from_frequencies(dictionary)
    else:
        name_string = " ".join(df["meal_name"])
        wordcloud = WordCloud(background_color="white",
                              width=w, 
                              height=h, 
                              colormap="Dark2",
                              collocations=True).generate(name_string)        
    return wordcloud

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('What are the most common dishes/per state?',style={'textAlign':'center'})
        ],width = 12)
    ]),
    dbc.Row([
            dbc.Col([
                    dbc.Select(options=[
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
                        ], value="Schleswig-Holstein", id="selector6",)    
            ]),
            ]),
    dbc.Row([
    dbc.Col(dbc.RadioItems(
                options=[
                    {"label": "Vegan", "value": "vegan"},
                    {"label": "Vegetarian", "value": "veget."},
                    {"label": "Omnivor", "value": "meat"},
                ],
                value="vegan", inline=True, id="selector7",),            
            ),
    ]), 
     dbc.Row([
        dbc.Col([
           dcc.Graph(id="graph11")     
        ])
    ]),
])
@callback(
      Output("graph11", "figure"), 
      Input("selector6","value"),
      Input("selector7","value")
)
def update_graph(value1, value2):
      return px.imshow(name_wordcloud(df,category = value2,state = value1))
