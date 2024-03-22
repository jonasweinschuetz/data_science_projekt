import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import json
import os

dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])
#os.chdir('C:/Users/Micro/Desktop/Neuer Ordner/data_science_projekt')
def get_canteen_domain(df):
    names = list(df["name"].str.findall(".+"))
    names = [names[0] for names in names]
    names = set(names)
    return names

# shows the weekly distribution of meal categories for each canteen
# in order to only show canteens that have big shifts between the percentage of meal categories between days
# only canteens where the highest standtart deviation between the percentage of categories surpases std_threshold are shown
# users can also limit the number of canteens shown and filter for canteens after state
def canteen_meal_distribution_after_std_threshold(df, std_threshold, max_show=200, state=""):
    if state == "Germany":
        state = ""
    #print(df)
    # if the user specify a state, querry a frame where only entries of this state appear 
    if state:
        df = df[df["state"] == state]
    
    df_filtered = df[df["vvo_percentage_max_std"] > std_threshold]
    #print(df_filtered)
    canteens = get_canteen_domain(df_filtered)
    
    i = 0
    figs = []
    for canteen in list(canteens):
        # check if (user specified) display limit is reached  
        if i > max_show-1:
            return figs
        
        # check if we have at least 15 entries for each weekday, removes outliers where to little data is available
        if not all(15 < df_filtered[df_filtered["name"] == canteen]["total_per_weekday"]):
            continue
            
        i += 1
        
        fig = px.bar(df_filtered[df_filtered["name"] == canteen], 
                     x="weekday",
                     y="vvo_percentage",
                     color="vvo_status",
                     color_discrete_map={'vegan':'darkgreen', 'veget.':'lightgreen', 'meat':'darkred'},
                     category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
                     text_auto=True,
                     #facet_row="name",
                     title=f"{i}Percentage of v/v/o meals each Weekday for {canteen}")
#fig.update_traces(textinfo= "label + percent entry")
        fig.update_layout(autosize=False,width=900,height=1*320,)
        figs.append(fig)
        
    return figs

df_germany = pd.read_csv('./data/data_webapp/rq5_df_germany.csv',sep='@',encoding='utf8')
df_canteen = pd.read_csv('./data/data_webapp/rq5_df_canteen.csv',sep='@',encoding='utf8')
df_state = pd.read_csv('./data/data_webapp/rq5_df_state.csv',sep='@',encoding='utf8')

fig1 = px.histogram(df_germany, 
             x="weekday",
             y="vvo_percentage",
             color="vvo_status",
             color_discrete_map={'vegan':'darkgreen', 'veget.':'lightgreen', 'meat':'darkred'},
             category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
             text_auto=True,
             title="Percentage of v/v/o meals each Weekday over all states")
fig1.update_layout(autosize=False,width=900,height=300,)

fig2 = px.bar(df_canteen[df_canteen["mensa_id"] == 1216], 
             x="weekday",
             y="vvo_percentage",
             color="vvo_status",
             color_discrete_map={'vegan':'darkgreen', 'veget.':'lightgreen', 'meat':'darkred'},
             category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
             text_auto=True,
             title=f"Percentage of v/v/o meals each Weekday in Kiel, Mensa I")
fig2.update_layout(autosize=False,width=900,height=300,)

layout = dbc.Container([
    dbc.Row([
            dbc.Col([
            dcc.Markdown('# 5. Do weekdays affect the variety of meal categories?',style={'textAlign':'center'})
        ],width = 12)
    ]),



    dbc.Row([
        dbc.Col([
           dcc.Markdown('''

         Firstly, we examined the distribution of the three VVO categories per weekday for our entire dataset. 

    ''',style={'textAlign':'center'})   
        ])
    ]),



    dbc.Row([
            dbc.Col([
            dcc.Graph(id="graph7",figure = fig1)
        ],width = 12)
    ]),
    dbc.Row([
            dbc.Col([
            dcc.Graph(id="graph8",figure = fig2)
        ],width = 12)
    ]),
        


    dbc.Row([
        dbc.Col([
           dcc.Markdown('''
    
            As expected, the distribution was fairly even. This is likely because patterns created by local regulations at the canteen level (e.g., Vegetarian Monday) tend to 'cancel out' when aggregated. Therefore, our next step was to take a closer look at our data and consider the canteens on a state level. Here two patterns emerged. In many countries (here, for example, Bavaria), the distribution remained fairly even. However, a surprising number of states had days with distinct outliers in their distribution (symbolized by Berlin and Brandenburg). These outliers are larger than can be explained by statistical noise. The hypothesis that in these states, canteens collectively offer fewer meat dishes on certain days is plausible. It is noteworthy that Berlin is the only one of these states where the outlier day has an increased offering of meat dishes. 

    ''',style={'textAlign':'center'})   
        ])
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
            ],value="Schleswig-Holstein",id="selector4",
            )],width = 12)
    ]),
    dbc.Row([
            dbc.Col([
            dcc.Graph(id="graph9")
        ],width = 12)
    ]),


    dbc.Row([
        dbc.Col([
           dcc.Markdown('''
    
            But this was not enough, we wanted to dig deeper. To get the full picture we need to look at each individual canteen. But it would be too exhausting to examine the graph for each of the over 600 canteens individually. Therefore, we calculated the standard deviation for each dish category for each canteen to use the largest of the three as a benchmark for the presence of a day-dependent category policy. This simple measure is suprisingly good, but definitely still has room for improvement. It is certainly helpful for sorting out uninteresting canteens whose weekday distributions are homogeneous amongst eachother. On the website, you will find a tool that allows you to search for canteens whose maximum VVO standard deviation exceeds a certain minimum value. Here are a few hand selected examples.

    ''',style={'textAlign':'center'})   
        ])
    ]),



   # dbc.Row([
   #        dbc.Col([
   #          dbc.Select(
   # options=[
    #    {"label": "Germany", "value": "Germany"},
    #    {"label": "Baden-Württemberg", "value": "Baden-Württemberg"},
   #     {"label": "Bayern", "value": "Bayern"},
    #    {"label": "Berlin", "value": "Berlin"},
    #    {"label": "Brandenburg", "value": "Brandenburg"},
    #    {"label": "Bremen", "value": "Bremen"},
    #    {"label": "Hamburg", "value": "Hamburg"},
    #   {"label": "Hessen", "value": "Hessen"},
    #    {"label": "Mecklenburg-Vorpommern", "value": "Mecklenburg-Vorpommern"},
    #    {"label": "Niedersachsen", "value": "Niedersachsen"},
    #    {"label": "Nordrhein-Westfalen", "value": "Nordrhein-Westfalen"},
    #    {"label": "Rheinland-Pfalz", "value": "Rheinland-Pfalz"},
    #    {"label": "Saarland", "value": "Saarland"},
    #    {"label": "Sachsen", "value": "Sachsen"},
    #    {"label": "Sachsen-Anhalt", "value": "Sachsen-Anhalt"},
    #    {"label": "Schleswig-Holstein", "value": "Schleswig-Holstein"},
     #   {"label": "Thüringen", "value": "Thüringen"},
    #], value="Germany",id="selector5",)
    #    ],width = 12)
   # ]),
   # dbc.Row([
    #        dbc.Col([
             #dbc.Input(placeholder="enter number between 0-2" ,id = "input1",min = 0,max =2, valid=True,value=2),
             #dbc.Input(placeholder="enter number between 0.0-20.0" ,id = "input2",min = 0,max =20, valid=True,value=8),
            
    #   ],width = 12)
    #]),
   # dbc.Row(id = "colum"),
])
@callback(
    Output("graph9", "figure"),
    #Output("colum", "children"),
    Input("selector4","value"),
    #Input("selector5","value"),
    #Input("input1","value"),
    #Input("input2","value")   
)
#def update_graph(value1,value2,value3,value4):
def update_graph(value1):
    fig_state = px.bar(df_state[df_state["state"] == value1], 
             x="weekday",
             y="vvo_percentage",
             color="vvo_status",
             color_discrete_map={'vegan':'darkgreen', 'veget.':'lightgreen', 'meat':'darkred'},
             category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
             text_auto=True,
             title="Percentage of v/v/o meals each Weekday in the state of "+value1)
    fig_state.update_layout(autosize=False,width=900,height=300,)
    
    #if (value3 == ''):
    #    value3 = 0
        
    #temp_int = float(value3)
    #temp_int = int(value3)
    
    #if (value4 == ''):
    #    value4 = 0
    
    #fig_temp = canteen_meal_distribution_after_std_threshold(df_canteen, float(value4), temp_int, value2)
   # res =[]
    
    #for i in range(len(fig_temp)):
     #   res += [dbc.Col([
      #      dcc.Graph(id="graph10_"+str(i),
      #      figure = fig_temp[i])
      #      ],width = 12)]
        
    return fig_state#,res 


