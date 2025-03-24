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

null_count_chart = dcc.Graph(id=landing_zone_cornea_configs.null_count_chart)

null_count_card = dmc.Card(
    children=[
        dmc.Text("Null Count Chart"),
        cornea_utils.get_loading_spinner(landing_zone_cornea_configs.null_count_loading_spinner),
        dmc.CardSection(null_count_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    px=30,
    style={"width": 1200, "height": 500, "margin": "20px"},
)

null_count_total_columns = dmc.Text(
    id=landing_zone_cornea_configs.null_count_total_columns,
    size="50px", weight="300"
)
null_count_all_feature_min_value = dmc.Text(
    id=landing_zone_cornea_configs.null_count_all_feature_min_value,
    size="50px", weight="300"
)
null_count_all_feature_max_value = dmc.Text(
    id=landing_zone_cornea_configs.null_count_all_feature_max_value,
    size="50px", weight="300"
)

null_count_insights_card = dmc.Card(
    children=[
        dmc.Text("Null Count Insights"),

        dmc.Divider(variant="solid"),
        dmc.Text("Total number of columns", size="20px", py=20),
        null_count_total_columns,

        dmc.Divider(variant="solid"),
        dmc.Text("Min null count value", size="20px", py=20),
        null_count_all_feature_min_value,

        dmc.Divider(variant="solid"),
        dmc.Text("Max null Value Count", size="20px", py=20),
        null_count_all_feature_max_value,
        dmc.Divider(variant="solid"),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 270, "height": 500, "margin": "20px"},
)

null_count_min_values_card = dmc.Card(
    children=[
        dmc.Text("Min values by features selected"),
        dmc.Divider(variant="solid"),
        html.Div(id=landing_zone_cornea_configs.null_count_min_values_card, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)

null_count_max_values_card = dmc.Card(
    children=[
        dmc.Text("Max values by features selected"),
        dmc.Divider(variant="solid"),
        html.Div(id=landing_zone_cornea_configs.null_count_max_values_card, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)


null_count_drift_card = dmc.Card(
    children=[
        dmc.Text("Drift values by features selected"),
        dmc.Divider(variant="solid"),
        html.Div(id=landing_zone_cornea_configs.null_count_drift_card, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)

null_count_content = html.Div([
    html.Div(
        [
            null_count_insights_card,
            null_count_card,
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
    dmc.Divider(),
    html.Div(
        [
            null_count_min_values_card,
            null_count_max_values_card,
            null_count_drift_card
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
])
