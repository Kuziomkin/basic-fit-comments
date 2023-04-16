from dash import html, Input, Output, callback, dcc
from .utils import filter_data, get_data
import plotly.graph_objects as go


#get data
df = get_data()


line_chart = html.Div(dcc.Graph(id="graph-line"))



#render barchart
@callback(
        Output("graph-line", "figure"),
    [
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value"),
        Input("period-slicer", "value")
    ]
)

def render_linechart(city, address, period):

    #filter data
    df_filtered = filter_data(df, city, address, period)

    #total positive comments per years
    pos_year = df_filtered.loc[df_filtered["Stars"] > 3].groupby(df_filtered["Date"].dt.year)["Stars"].count()
    #tottal negative comments per years
    neg_year = df_filtered.loc[df_filtered["Stars"] < 3].groupby(df_filtered["Date"].dt.year)["Stars"].count()
    #total neutral comments per years
    neu_year = df_filtered.loc[df_filtered["Stars"] == 3].groupby(df_filtered["Date"].dt.year)["Stars"].count()
    #total comments per years
    all_year = df_filtered.groupby(df_filtered["Date"].dt.year)["Stars"].count()
    #positive rate
    pos_rate = pos_year / all_year
    #negative rate
    neg_rate = neg_year / all_year
    #neutral rate
    neu_rate = neu_year / all_year


    #define chart data
    data1_line = go.Scatter(
        x = neg_rate.index,
        y = neg_rate.values,
        name="negative ( < 3 Stars)",
        line=dict(
            color="#ffd2b0"
        )
    )

    data2_line = go.Scatter(
        x = pos_rate.index,
        y = pos_rate.values,
        name = "positive ( > 3 Stars)",
        line=dict(
            color="#fe7000"
        )
    )

    data3_line = go.Scatter(
        x = neu_rate.index,
        y = neu_rate.values,
        name = "neutral ( = 3 Stars)",
        line=dict(
            color="gray"
        )
    )

    #define layout
    layout_line_chart = go.Layout(
        title = dict(
            text="<b>Comments Stars Ratioт Per Years<b>",
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
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis = dict(
            showgrid = False,
            showline = False,
            title="Year"
        ),
        yaxis = dict(
            showgrid = False,
            showline = False,
            title="Percentage"
        ),
        showlegend=True
    )

    line_chart = go.Figure(data=[data1_line, data2_line, data3_line], layout=layout_line_chart)

    return line_chart