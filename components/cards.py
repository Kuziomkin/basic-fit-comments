from dash import html, Input, Output, callback, callback_context
from .utils import filter_data, get_data
import decimal


#get data
df = get_data()


#create html elements
cards = html.Div(
            children=[
                html.Div(
                    children=[
                        html.Label(children= "Total Reviews", className="settings-title"),
                        html.P(
                            html.Label(children= "Avg. Rating", className="card-text", id = "tot-rev-id")
                        )
                    ],
                    className="total-review-card"
                ),
                html.Div(
                    children=[
                        html.Label(children= "Avg. Rating", className="settings-title"),
                        html.P(
                            html.Label(children= "Avg. Rating", className="card-text", id = "avg-rating-id")
                        )
                    ],
                    className="avg-rating-card"
                ),
                html.Div(
                    children=[
                        html.Label(children= "Pct. Positive", className="settings-title"),
                        html.P(
                            html.Label(children= "Avg. Rating", className="card-text", id = "pct-positive-id")
                        )
                    ],
                    className="pct-positive"
                ),
                html.Div(
                    children=[
                        html.Label(children= "Pct. Negative", className="settings-title"),
                        html.P(
                            html.Label(children= "Avg. Rating", className="card-text", id = "pct-negative-id")
                        )
                    ],
                    className="pct-negative"
                )
            ],
            className="card-fields"
        )


#cards handler
@callback(
    [
        Output("tot-rev-id", "children"),
        Output("avg-rating-id", "children"),
        Output("pct-positive-id", "children"),
        Output("pct-negative-id", "children"),
    ],
    [
        Input("city-dropdown", "value"),
        Input("address-dropdown", "value"),
        Input("period-slicer", "value")
    ]
)

def render_cards(city, address, period):
    
    df_filtered = filter_data(df, city, address, period)
    children_total_rev = df_filtered["Reviews"].count() 
    
    if df_filtered.empty:
        children_total_rev = 0.0
        children_avg_rat = 0.0
        children_pos_rate = "0.0 %"
        children_neg_rate = "0.0 %"
    else:
        #prepare data to return
        children_avg_rat = df_filtered["Stars"].mean().astype(float).round(1)
            
        #total positive comments
        pos = df_filtered.loc[df_filtered["Stars"] > 3]["Stars"].count()
        #tottal negative comments
        neg = df_filtered.loc[df_filtered["Stars"] < 3]["Stars"].count()
        #total comments
        all_data = df_filtered["Stars"].count()
        #positive rate
        children_pos_rate = str(decimal.Decimal(pos / all_data).quantize(decimal.Decimal('0.000')) * 100)[:-2] + "%"
        #negative rate
        children_neg_rate = str(decimal.Decimal(neg / all_data).quantize(decimal.Decimal('0.000')) * 100)[:-2] + "%"

    return children_total_rev, children_avg_rat, children_pos_rate, children_neg_rate
