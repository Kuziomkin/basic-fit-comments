from dash import html, Input, Output, callback, dcc, dash_table
from .utils import filter_data, get_data
import plotly.graph_objects as go


#get data
df = get_data()

# dash tables
# table columns to render
columns = [
    {"name": "Address", "id": "Address"},
    {"name": "Author", "id": "Author"},
    {"name": "Date", "id": "Date"},
    {"name": "Stars", "id": "Stars"},
    {"name": "Comment", "id": "Comment"}
]


# table settings
d_table = dash_table.DataTable(
    id='table',
    columns=columns, 
    page_size=10,
    style_cell={
        'maxWidth': 226,
        'whiteSpace': 'normal',
        'height': 'auto',
    },
    style_cell_conditional=[
        {'if': {'column_id': 'Address'},
         'width': '20%'},
        {'if': {'column_id': 'Author'},
         'width': '15%'},
        {'if': {'column_id': 'Date'},
         'width': '15%'},
        {'if': {'column_id': 'Stars'},
         'width': '5%'},
        {'if': {'column_id': 'Comment'},
         'width': '45%'},
    ],
    style_data={
        'textAlign': 'left'
    },
)


#tabs element
selected_style = {
    'borderTop': "6px solid #fe7000",
    'borderBottom': "2px solid #d6d6d6",
    'borderRight': '2px solid #d6d6d6',
    'borderLeft': '2px solid #d6d6d6',
    'fontWeight': 'bold',
    "color" : "black",
    'padding': '6px',
    'justify-content': 'center',
    'border-radius': '12px',
    "font-style" : "oblique",
    "height" : "60px"
}

#tavle tabs
table_tabs = dcc.Tabs(
    id = "table_tabs",
    value="all-tab",
    children=[
        dcc.Tab(
            label="All Comments",
            value="all-tab",
            style = {
                "color" : "#A9A9A9",
                'padding': '6px',
                'justify-content': 'center',
                'border-radius': '6px',
            },
            selected_style=selected_style
        ),
        dcc.Tab(
            label="Positive Comments",
            value="positive-tab",
            style = {
                "color" : "#A9A9A9",
                'padding': '6px',
                'justify-content': 'center',
                'border-radius': '6px',
            },
            selected_style=selected_style
        ),
        dcc.Tab(
            label="Negative Comments",
            value="negative-tab",
            style = {
                "color" : "#A9A9A9",
                'padding': '6px',
                'justify-content': 'center',
                'border-radius': '6px',
            },
            selected_style=selected_style
        ),  
        dcc.Tab(
            label="Neutral Comments",
            value="neutral-tab",
            style = {
                "color" : "#A9A9A9",
                'padding': '6px',
                'justify-content': 'center',
                'border-radius': '6px',

            },
            selected_style=selected_style
        )
    ],
    colors={
        "primary": "white",
    },
    className = "table_tabs",
    style = {
        'height': '20px'
    }

)

#html element to render
table = html.Div(children=[
    html.Div(table_tabs),
    html.Div(d_table, className="table-div") 
]) 


#render table
@callback(
        Output("table", "data"),
    [
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value"),
        Input("period-slicer", "value"),
        Input("table_tabs", "value")
    ]
)

def render_table(city, address, period, tab_value):

    #filter data
    df_filtered = filter_data(df, city, address, period)

    #data for tables
    if tab_value == "all-tab":
       tables_data = (
        df_filtered
        [["Address","Author","Date","Stars","Comment"]]
        .sort_values(by=["Date"], ascending=False)
        .to_dict(orient='records')) 
    elif tab_value == "positive-tab":
        tables_data = (
            df_filtered.loc[
                df_filtered["Stars"] > 3
            ]
            [["Address","Author","Date","Stars","Comment"]]
            .sort_values(by=["Date"], ascending=False)
            .to_dict(orient='records'))
    elif tab_value == "negative-tab":
        tables_data = (
            df_filtered.loc[
                df_filtered["Stars"] < 3
            ]
            [["Address","Author","Date","Stars","Comment"]]
            .sort_values(by=["Date"], ascending=False)
            .to_dict(orient='records'))
    elif tab_value == "neutral-tab":
        tables_data = (
            df_filtered.loc[
                df_filtered["Stars"] == 3
            ]
            [["Address","Author","Date","Stars","Comment"]]
            .sort_values(by=["Date"], ascending=False)
            .to_dict(orient='records'))

    return tables_data