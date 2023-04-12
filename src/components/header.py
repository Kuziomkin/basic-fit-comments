from dash import html


style_line = {
    "position": "relative",
    "background-color": "#fe7000",
    "height": "40px",
    "display": "flex"
}

style_title = {
    "position": "relative",
    "color": "#2d2d2d",
    "margin": "20px auto",
    "text-align": "center",
    "font-weight":"200",
    "font-family": "HeadingProDouble-Regular,sans-serif",
    "background-color": "#fff"
}


header = html.Div(
    children=[
        html.Div(
            style = style_line
            ),
        html.H1(
            children="Basic-Fit Comments Analysis",
            className="title-header",
            style=style_title
            ),
        html.Div(
            style = style_line
            )
    ]
)