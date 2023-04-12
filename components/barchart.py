from dash import html, Input, Output, callback, dcc
from .utils import filter_data, get_data
import plotly.graph_objects as go


#get data
df = get_data()


bar_chart = html.Div(dcc.Graph(id="graph-bar"))


#render barchart
@callback(
        Output("graph-bar", "figure"),
    [
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value"),
        Input("period-slicer", "value")
    ]
)

def render_barchart(city, address, period):

    #filter data
    df_filtered = filter_data(df, city, address, period)

    #prepare axis data
    x = df_filtered["Address"].sort_values().unique()
    y = df_filtered[["Address", "Stars"]].groupby(by="Address").mean().sort_values(by="Address")["Stars"]
    if df_filtered.count()["Address"] != 0:
        y = y.astype(float).round(1)
    #create diagram
    data_bar = go.Bar(
        x = x,
        y = y,
        marker_color = "#ffd2b0",
        marker_line_color = "gray",
        marker_line_width = 1,
        opacity=0.5,
        text = y,
        textposition='inside'
    )

    layout_bar_chart = go.Layout(
        title = dict(
            text ="<b>Total Gym Rating<b>",
            x=0.5,
            y=0.92,
            xanchor= 'center',
            yanchor= 'top'
            ),
        font = dict(
            family="HeadingProDouble-Regular,sans-serif",
            size=14,
            color="black"
            ),
        width=500,
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis = dict(
            showgrid = False,
            showline = False,
            tickangle=-45,
            
        ),
        yaxis = dict (
            showgrid = False,
            showline = False,
            title="Rating"
        )
    )
    bar_chart = go.Figure(data=data_bar, layout=layout_bar_chart)

    return bar_chart
