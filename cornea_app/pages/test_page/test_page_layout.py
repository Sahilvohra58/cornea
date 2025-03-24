from dash import html
import dash_mantine_components as dmc

from pages.test_page.test_page_components import histogram_plot_card

test_page_layout = html.Div([
    html.Div(
        [
            histogram_plot_card
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    )
])
