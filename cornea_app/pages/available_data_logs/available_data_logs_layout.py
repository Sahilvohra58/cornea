from dash import html
import dash_mantine_components as dmc

from pages.available_data_logs.available_data_logs_components import available_data_page_layout, \
    available_data_input

available_data_layout = html.Div([
    html.Div(
        [
            available_data_input
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
    dmc.Divider(variant="solid"),
    html.Div(
        [
            available_data_page_layout
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
])
