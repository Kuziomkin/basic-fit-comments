from dash import Dash, dcc, html, Input, Output, callback
from dash.exceptions import PreventUpdate
import pandas as pd
from .utils import filter_data, get_data


#get data
df = get_data()


button = html.Div(
    children=[
        html.Br(),
        html.P(children=[
                    html.Label("Download CSV", id="btn_csv", n_clicks=0, style={"border-style": "solid", "border-radius": "2px", "border-width": "1px", "border-color": "gray", "padding": "5px", "margin-left": "90px"}),
        ]),
        dcc.Download(id="download-dataframe-csv")
    ]
)



@callback(
    [
        Output("download-dataframe-csv", "data"),
        Output("btn_csv", "n_clicks"),
    ],

    [
        Input("btn_csv", "n_clicks"),
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value"),
        Input("period-slicer", "value")
    ],
    prevent_initial_call=True,
)
def func(n_clicks, city, address, period):
    #filter data
    df_filtered = filter_data(df, city, address, period)
    if n_clicks == 1:
        n_clicks = 0
        return dcc.send_data_frame(df_filtered.to_csv, "mydf.csv"), n_clicks
    else:
        return None, n_clicks 


