from dash import html, Input, Output, callback, dcc
from .utils import filter_data, get_data
import plotly.graph_objects as go


#get data
df = get_data()


scatter_chart = html.Div(dcc.Graph(id="graph-scatter"))


#render barchart
@callback(
        Output("graph-scatter", "figure"),
    [
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value"),
        Input("period-slicer", "value")
    ]
)

def render_scatterchart(city, address, period):

    #filter data
    df_filtered = filter_data(df, city, address, period)

    data_scatter = go.Scatter(
        x = df_filtered.groupby(by=["Address"]).count().sort_values(by="Address")["Reviews"].values,
        y = df_filtered[["Address", "Stars"]].groupby(by=["Address"]).mean().sort_values(by="Address")["Stars"].values.round(1),
        text=df_filtered["Address"].sort_values().unique(),
        mode='markers',
        marker=dict(
            color=df_filtered.groupby(by=["Address"])["Stars"].mean().values.round(1),
            size=df_filtered.groupby(by=["Address"])["Stars"].mean().values.round(1) * 10,
            showscale=True,
            colorscale="ylorrd"
        )
    )

    layout_scatter_chart = go.Layout(
        title=dict(
            text="<b>Total Gym Rating Vs Amount Of Reviews<b>",
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
        xaxis=dict(
            showgrid=False,
            showline=False,
            title="Reviews"
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            title="Rating"
        )
    )

    scatter_chart = go.Figure(data=data_scatter, layout=layout_scatter_chart)

    return scatter_chart
