import dash
from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import json


dash.register_page(__name__, external_stylesheets =[dbc.themes.BOOTSTRAP])

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


path_data = "./data/german-canteens(filtered).csv"
path_geo = './data/further_updated_german_canteens.json'
data = pd.read_csv(path_data,sep="@",index_col=0) 
geo_data = pd.read_json(path_geo ,encoding='utf8')

data.drop(['employee_price', 'student_price', "guest_price", "meal_id"], axis=1, inplace=True)
data = data[data["vvo_status"] != "-1"]

data["date"] = pd.to_datetime(data["date"])
data["weekday"] = data["date"].dt.day_name()
data = data[data["weekday"].isin(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]

data = data.join(geo_data.set_index('id'),on='mensa_id')
data.drop(["address", "coordinates", "state-id"], axis=1, inplace=True)

df_germany = data
german_count_per_weekday = df_germany[["state", "weekday", "meal_name"]].groupby(["state", "weekday"]).count().rename(columns={"meal_name": "total_per_weekday"})
vvo_german_count_per_weekday = df_germany[["state", "vvo_status", "weekday", "meal_name"]].groupby(["state", "vvo_status", "weekday"]).count().rename(columns={"meal_name": "total_per_weekday_per_vvo"})

df_germany = vvo_german_count_per_weekday.join(german_count_per_weekday, on=["state", "weekday"], how="inner")
df_germany["vvo_percentage"] = df_germany["total_per_weekday_per_vvo"]/df_germany["total_per_weekday"]
df_germany = df_germany.reset_index()

df_germany["vvo_percentage"] = df_germany["vvo_percentage"].map(lambda x: 100*round(x, 4))
df_germany["vvo_percentage"] = df_germany["vvo_percentage"].map(lambda x: x/15)

df_state = data[:]
state_count_per_weekday = df_state[["state", "weekday", "meal_name"]].groupby(["state", "weekday"]).count().rename(columns={"meal_name": "total_per_weekday"})

vvo_state_count_per_weekday = df_state[["state", "vvo_status", "weekday", "meal_name"]].groupby(["state", "vvo_status", "weekday"]).count().rename(columns={"meal_name": "total_per_weekday_per_vvo"})

df_state = vvo_state_count_per_weekday.join(state_count_per_weekday, on=["state", "weekday"], how="inner")
df_state["vvo_percentage"] = df_state["total_per_weekday_per_vvo"]/df_state["total_per_weekday"]
df_state = df_state.reset_index()
df_state["vvo_percentage"] = df_state["vvo_percentage"].map(lambda x: 100*round(x, 4))

df_canteen = data
df_canteen = df_canteen.groupby(["name", "mensa_id", "state", "weekday", "vvo_status"]).count().reset_index()

canteen_count_per_weekday = df_canteen[["name", "mensa_id","state", "weekday", "meal_name"]].groupby(["name", "mensa_id", "state", "weekday"]).sum().rename(columns={"meal_name": "total_per_weekday"})

canteen_vvo_count_per_weekday = df_canteen[["name", "mensa_id", "state", "vvo_status", "weekday", "meal_name"]].groupby(["name", "mensa_id", "state", "vvo_status", "weekday"]).sum().rename(columns={"meal_name": "total_per_weekday_per_vvo"})

df_canteen = canteen_vvo_count_per_weekday.join(canteen_count_per_weekday, on=["name", "mensa_id", "state", "weekday"], how="inner", rsuffix="_")
df_canteen["vvo_percentage"] = df_canteen["total_per_weekday_per_vvo"]/df_canteen["total_per_weekday"]
df_canteen = df_canteen.reset_index()
df_canteen["vvo_percentage"] = df_canteen["vvo_percentage"].map(lambda x: 100*round(x, 4))

std_vvo_percentage = df_canteen.groupby(["name", "state", "vvo_status"]).std(numeric_only=True)["vvo_percentage"] # weekbased standart deviantion of vvo_percentage 

max_std_vvo_percentage = std_vvo_percentage.groupby(["name", "state"]).max()

df_canteen = df_canteen.join(std_vvo_percentage, on=["name", "state", "vvo_status"], rsuffix="_std")
df_canteen = df_canteen.join(max_std_vvo_percentage, on=["name", "state"], rsuffix="_max_std")

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
            dcc.Markdown('Do weekdays affect the variety of meal categories?',style={'textAlign':'center'})
        ],width = 12)
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
             dbc.Select(
    options=[
        {"label": "Germany", "value": "Germany"},
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
    ], value="Germany",id="selector5",)
        ],width = 12)
    ]),
    dbc.Row([
            dbc.Col([
             dbc.Input(placeholder="enter number between 0-50" ,id = "input1",min = 0,max =50, valid=True,value=5),
             dbc.Input(placeholder="enter number between 0.0-20.0" ,id = "input2",min = 0,max =20, valid=True,value=8),
             
        ],width = 12)
    ]),
    dbc.Row(id = "colum"),
])
@callback(
    Output("graph9", "figure"),
    Output("colum", "children"),
    Input("selector4","value"),
    Input("selector5","value"),
    Input("input1","value"),
    Input("input2","value")   
)
def update_graph(value1,value2,value3,value4):
    fig_state = px.bar(df_state[df_state["state"] == value1], 
             x="weekday",
             y="vvo_percentage",
             color="vvo_status",
             color_discrete_map={'vegan':'darkgreen', 'veget.':'lightgreen', 'meat':'darkred'},
             category_orders=dict(weekday=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
             text_auto=True,
             title="Percentage of v/v/o meals each Weekday in the state of "+value1)
    fig_state.update_layout(autosize=False,width=900,height=300,)
    
    if (value3 == ''):
        value3 = 0
        
    temp_int = float(value3)
    temp_int = int(value3)
    
    if (value4 == ''):
        value4 = 0
    
    fig_temp = canteen_meal_distribution_after_std_threshold(df_canteen, float(value4), temp_int, value2)
    res =[]
    
    for i in range(len(fig_temp)):
        res += [dbc.Col([
            dcc.Graph(id="graph10_"+str(i),
            figure = fig_temp[i])
            ],width = 12)]
        
    return fig_state,res 


