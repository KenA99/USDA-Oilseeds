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
    html.H1("USDA Oilseeds Data Dashboard"),
    html.H2("Created using Plotly Dash"),
    html.P(["This data was pulled from the United States Department of Agriculture Foreign Agriculture Service (USDA FSA) Production, \
        Supply and Distribution (PSD) online database using the custom query to create an Excel document that was then converted to a CSV file. \
        This data can be found at the ", 
    html.A("USDA FSA PSD",href = "https://apps.fas.usda.gov/psdonline/app/index.html#/app/home", 
        target="_blank")," website"]),
    html.P(["The data here shows graphs for the last 10 years for popular oilseed crops throughout the globe offering a visual of how their production has changed\
        over time using variables from a ", html.A("Supply Distribution Table", href ="https://apps.fas.usda.gov/psdonline/app/index.html#/app/about#G4"), " that shows Supply in the form of beginning stocks, domestic production, and imports; and\
        Use through domestic consumption, exports, and ending stocks. Stocks can be considered any kind of storage of commodities not being used from\
        from waiting to be processed to a farmer holding on to a crop for high prices to sell."]),
    
    html.Br(),
    html.Br(),

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
                labels={
                    "Year":"Market Year",
                    "value": "1000 Metric Tons",
                    "variable":"Oilseed Crop"
                },
                title=f"{', '.join(crop_select)} oilseed {attribute_select} in {country_select} from 2012-2022"
                )
    
    return fig

if __name__ =='__main__':
    app.run_server(debug=True)

