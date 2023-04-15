from dash import html, dcc, Input, Output, callback, callback_context
import pandas as pd
from components.utils import create_dic, get_data
from components.downloadbutton import button
from .utils import filter_adresses


#get data
df = get_data()

#create address dict
address_dict = create_dic(df)

#create range-slicer
slicer = dcc.RangeSlider(
    min = df["Date"].dt.year.unique().min() - 2000,
    max = df["Date"].dt.year.unique().max() - 2000,
    step = 1,
    value = [df["Date"].dt.year.unique().min() - 2000, df["Date"].dt.year.unique().max() - 2000],
    id='period-slicer',
    marks={
        12 : "2012",
        
        14 : "2014",
        
        16 : "2016",
        
        18 : "2018",
       
        20 : "2020",
        
        22 : "2022",
        23 : "2023",
    },
    className="period-slicer",
    
)


#cities dropdown
city_dropdown = dcc.Dropdown(
    options=df["City"].unique(), 
    value=df[df["City"] == "Madrid"]["City"].unique(), 
    id="city-dropdown", 
    multi=True,
    className="city-dropdown"
)


#city radio buttoms
city_radioitems = dcc.RadioItems(
    ['All', 'Customize', "Reset"],
    value ='Customize',
    className="city-radioitems",
    id = "city-radioitems",
    inputStyle={
        "margin-right": "10px"
        },
    labelStyle={
        "margin-right" : "10px"
    }
)


#address dropdown
address_dropdown = dcc.Dropdown(
    options=df["Address"].unique(),
    value=df[df["City"] == "Madrid"]["Address"].unique(),
    id="address-dropdown",
    multi=True,
    className="address-dropdown"
)

#address radio buttoms
address_radioitems = dcc.RadioItems(
    ['All', 'Customize', "Reset"],
    value='All',
    className="address-radioitems",
    id = "address-radioitems",
    inputStyle={
        "margin-right": "10px"
        },
    labelStyle={
        "margin-right" : "10px"
    }
)



setting_form =  html.Div(
            children=[
                html.Form(
                    children=[
                        html.Fieldset(
                            children=[
                                html.Div(
                                    children=[
                                        html.Label(children= "Select Time Period", className="settings-title"),
                                        html.P(slicer)
                                    ],
                                    className="period-div",
                                    id = "period-id"
                                ),
                                html.Div(
                                    children=[
                                        html.Label(children= "Select Cities", className="settings-title"),
                                        html.P(city_dropdown)
                                    ],
                                    className="city-dropdown-div",
                                    id = "city-dropdown-id"
                                ),
                                html.Div(
                                    children=[
                                        html.Label(children= "Filter Cities", className="settings-title"),
                                        html.P(city_radioitems)
                                    ],
                                    className="city-radioitems-div",
                                    id = "city-radioitems-id"
                                ),
                                html.Div(
                                    children=[
                                        html.Label(children= "Select Gyms Address", className="settings-title"),
                                        html.P(address_dropdown)
                                    ],
                                    className="address-dropdown-div",
                                    id = "address-dropdown-id"
                                ),
                                html.Div(
                                    children=[
                                        html.Label(children= "Filter Address", className="settings-title"),
                                        html.P(address_radioitems)
                                    ],
                                    className="address-radioitems-div",
                                    id = "address-radioitems-id"
                                ),
                                button
                            ],
                            className="settings-fieldset",
                            style={
                                "position":"relative",
                                "width": "340px",
                                "top":"40px",
                                "border-style":"double"
                            }
                        )
                    ]    
                )
            ],
            className="settings-div"
        )


#forms handler
@callback(
    [
        Output("city-radioitems", "value"),
        Output("city-dropdown", "value"),
        Output("address-radioitems", "value"),
        Output("address-dropdown", "value"),
        Output("address-dropdown", "options")
    ],
    [
        Input("address-radioitems", "value"),
        Input("address-dropdown", "value"),
        Input("address-dropdown", "options"),
        Input("city-radioitems", "value"),
        Input("city-dropdown", "value")
    ]
)

def filter_forms(address_set, address_values, address_options, city_set, city_values):
    #filter address radio button
    input_id = callback_context.triggered[0]["prop_id"].split(".")[0]
    if input_id == "city-radioitems":
        if city_set == "All":
            city_values = df["City"].unique()
            address_options = df["Address"].unique()
            address_set = "Customize"
        elif city_set == "Reset":
            city_values = None
            address_values = None
            address_set = "Reset"
    if input_id == "address-radioitems":
        if address_set == "All":
            if city_values != None:
                address_values = df.loc[df["City"].isin(city_values),"Address"].unique()
            else:
                address_values = None
        elif address_set == "Reset":
            address_values = None
            if city_values != None:
                address_options = df.loc[df["City"].isin(city_values),"Address"].unique()
            else:
                address_options = None
    if input_id == "city-dropdown":
        if  city_values != None:
            address_options = df.loc[df["City"].isin(city_values),"Address"].unique()
            if address_values == None or len(address_values) == 0:
                address_set = "Reset"
            elif set(address_values) != set(address_options):
                address_set = "Customize"
        elif city_values == None or len(city_values) == 0:
            address_options = df["Address"].unique()
        if set(city_values) == set(df["City"].unique()):
            city_set = "All"
        elif city_values == None or len(city_values) == 0:
            city_set = "Reset"
        else:
            city_set = "Customize"
    if input_id == "address-dropdown":
        if set(address_values) == set(address_options):
            address_set = "All"
        elif address_values == None or len(address_values) == 0:
            address_set = "Reset"
        else:
            address_set = "Customize"
        if address_values != None:
            city_values = [k for k, v in address_dict.items() if any(item in v for item in address_values)]
            if len(city_values) == 0:
                city_set = "Reset" 
            elif set(city_values) != set(df["City"].unique()):
                city_set = "Customize"

    return city_set, city_values, address_set, address_values, address_options


#range slider handler
#cards handler
@callback(
        Output("period-slicer", "value"),
    [
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value")
    ]
)
def render_slider(city, address):
    
    #filter data
    df_filtered = filter_adresses(df, city, address)
    if df_filtered.empty:
        value = [df["Date"].dt.year.unique().min() - 2000, df["Date"].dt.year.unique().max() - 2000]
    else:
        value = [df_filtered["Date"].dt.year.unique().min() - 2000, df_filtered["Date"].dt.year.unique().max() - 2000]

    return value
