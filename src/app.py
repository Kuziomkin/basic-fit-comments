from dash import Dash, dcc, html, Input, Output, callback_context, dash_table
import plotly.graph_objects as go
import pandas as pd
from components.header import header
from components.form import setting_form
from components.cards import cards
from components.barchart import bar_chart
from components.scatterchart import scatter_chart
from components.linechart import line_chart
from components.table import table
from components.footer import footer


#run app
app = Dash(__name__)


#html page
app.layout = html.Div(
    children=[
        header,
        html.Div(
            children=[
                setting_form,
                html.Div(
                    children=[
                        cards,
                        bar_chart,
                        scatter_chart,
                        line_chart,
                        table,
                        
                    ],
                ),
            ],
        className= "body-div"
        ),
        footer
    ]
)


if __name__ == "__main__":
    app.run_server(debug=False, dev_tools_hot_reload=True)