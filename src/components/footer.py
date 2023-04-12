from dash import html, dcc


style_line = {
    "position": "relative",
    "background-color": "#fe7000",
    "height": "40px",
    "display": "flex",
}


footer = html.Div(
    children=[
        html.Div(style=style_line, className="footer-div"),
        html.Div(html.H6(["©2023, Developed By ", html.A("Dzianis Kuziomkin" , href="https://www.linkedin.com/in/dzianis-kuziomkin/", target="_blank",style={"color": "#0084d6"})]))
    ],
)