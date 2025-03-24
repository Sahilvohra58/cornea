from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Live adjustable subplot-width'),
    dcc.Graph(id="graph"),
    html.P("Subplots Width:"),
    dcc.Slider(
        id='slider-width', min=.1, max=.9,
        value=0.5, step=0.1)
])


@app.callback(
    Output("graph", "figure"),
    Input("slider-width", "value"))
def customize_width(left_width):
    import json
    f = open('config.json')
    data = json.load(f)
    no_cols = data['no_figs']

    temp_list = [1] * (data['no_figs'] - 1)
    remaining_charts_width_list = [(x * ((1 - left_width) / (no_cols - 1))) for x in temp_list]

    fig = make_subplots(rows=1, cols=data['no_figs'],
                        column_widths=[left_width] + remaining_charts_width_list
                        )

    for n in range(data['no_figs']):
        fig.add_trace(
            row=1,
            col=n + 1,
            trace=go.Bar(x=[1, 2, 3] * (10 ** (n + 1)), y=[4, 5, 6] * (10 ** (n + 1))) if data.get(
                "plot_type") == "bar" else go.Scatter(
                x=[1, 2, 3] * (10 ** (n + 1)),
                y=[4, 5, 6] * (10 ** (n + 1))
            ))

    return fig


app.run_server(debug=True, port="9950")
