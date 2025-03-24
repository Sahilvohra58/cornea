from dash import dcc, html
import dash_mantine_components as dmc
from google.cloud import firestore

from pages.landing_zone.landing_zone_cornea_configs import LandingZoneCorneaConfigs
from cornea_utils import CorneaUtils

cornea_utils = CorneaUtils()
landing_zone_cornea_configs = LandingZoneCorneaConfigs()

firestore_client = firestore.Client(
    project=landing_zone_cornea_configs.cornea_configs.project_id,
    database=landing_zone_cornea_configs.cornea_configs.firestore_database
)

min_values_chart = dcc.Graph(id=landing_zone_cornea_configs.min_values_chart)

min_values_card = dmc.Card(
    children=[
        dmc.Text("Min Values Chart"),
        cornea_utils.get_loading_spinner(landing_zone_cornea_configs.min_values_loading_spinner),
        dmc.CardSection(min_values_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    px=30,
    style={"width": 1500, "height": 500, "margin": "20px"},
)


min_values_min_values_card = dmc.Card(
    children=[
        dmc.Text("Min values by features selected"),
        dmc.Divider(variant="solid"),
        html.Div(id=landing_zone_cornea_configs.min_values_min_values_card, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)

min_values_max_values_card = dmc.Card(
    children=[
        dmc.Text("Max values by features selected"),
        dmc.Divider(variant="solid"),
        html.Div(id=landing_zone_cornea_configs.min_values_max_values_card, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)


min_values_drift_card = dmc.Card(
    children=[
        dmc.Text("Drift values by features selected"),
        dmc.Divider(variant="solid"),
        html.Div(id=landing_zone_cornea_configs.min_values_drift_card, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)

min_values_content = html.Div([
    html.Div(
        [
            min_values_card
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
    dmc.Divider(),
    html.Div(
        [
            min_values_min_values_card,
            min_values_max_values_card,
            min_values_drift_card
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
])
