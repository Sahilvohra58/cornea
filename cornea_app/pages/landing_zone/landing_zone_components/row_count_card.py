from dash import dcc
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

row_count_chart = dcc.Graph(id=landing_zone_cornea_configs.row_count_chart, style={"padding": "20px"})

row_count_card = dmc.Card(
    children=[
        dmc.Text("Row Count Chart"),
        cornea_utils.get_loading_spinner(landing_zone_cornea_configs.row_count_loading_spinner),
        dmc.CardSection(row_count_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 1200, "height": 500, "margin": "20px"},
)

row_count_total_records = dmc.Text(
    id=landing_zone_cornea_configs.row_count_total_records,
    size="50px", weight="300"
)
row_count_min_value = dmc.Text(
    id=landing_zone_cornea_configs.row_count_min_value,
    size="50px", weight="300"
)
row_count_max_value = dmc.Text(
    id=landing_zone_cornea_configs.row_count_max_value,
    size="50px", weight="300"
)

row_count_insights_card = dmc.Card(
    children=[
        dmc.Text("Row Count Insights"),

        dmc.Divider(variant="solid"),
        dmc.Text("Total number of records", size="20px", py=20),
        row_count_total_records,

        dmc.Divider(variant="solid"),
        dmc.Text("Min row value count", size="20px", py=20),
        row_count_min_value,

        dmc.Divider(variant="solid"),
        dmc.Text("Max row value Count", size="20px", py=20),
        row_count_max_value,
        dmc.Divider(variant="solid"),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 270, "height": 500, "margin": "20px"},
)
