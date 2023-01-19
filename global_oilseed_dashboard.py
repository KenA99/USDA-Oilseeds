import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# intialize the app
app = Dash(__name__)

# import the data from inside the directory
df = pd.read_csv("global_oilseed_2012-2022.csv")

# drop the unit description since it is standard
df = df.drop(columns="Unit Description")

# rename the headers to an easier naming convention
df = df.rename(columns={"Oilseed, Peanut":"Peanut", "Oilseed, Rapeseed":"Rapeseed", "Oilseed, Soybean":"Soybean", 
    "Oilseed, Soybean (Local)": "Local Soybean", "Oilseed, Sunflowerseed":"Sunflowerseed"})

# add variable names for the graph axes
# country_select = ""


# filter the data to clean it for the graph


headers = df.columns.values.tolist()
crop_options = headers[3:]

country_names = df["Country"].drop_duplicates().sort_values().tolist()
attribute_names = df["Attribute"].drop_duplicates().sort_values().tolist()

# page layout in HTML
app.layout = html.Div([
    html.H1("Web Application Dashboard for USDA Oilseeds using Dash"),

dcc.Dropdown(id="country_name", options= country_names, multi= False, placeholder = "Select a Country", style= {'width': "40%"}),
dcc.Checklist(id="oilseed_crops", options=crop_options, value=[crop_options[0]]),
dcc.RadioItems(id="attribute", options=attribute_names, value= attribute_names[0]),


dcc.Graph(id="oilseed_graph", figure= {})
])

# connecting the Plotly graphs with the Dash components
@app.callback(
    Output(component_id='oilseed_graph', component_property='figure'),
    Input(component_id="country_name", component_property= 'value'),
    Input(component_id="oilseed_crops", component_property="value"),
    Input(component_id="attribute", component_property="value")
)

def update_graph(country_select,crop_select, attribute_select):
    
    # attribute_select = "Beginning Stocks"

    filtered_df = df.loc[(df["Country"] == country_select) & (df["Attribute"] == attribute_select)]

    fig = px.line(filtered_df, 
                x="Year", 
                y= crop_select,
                title=f"{', '.join(crop_select)} oilseed {attribute_select} in {country_select} from 2012-2022"
                )
    
    return fig

if __name__ =='__main__':
    app.run_server(debug=True)

