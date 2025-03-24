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

landing_zone_schema_piechart = dcc.Graph(id=landing_zone_cornea_configs.landing_zone_schema_piechart)

landing_zone_schema_piechart_card = dmc.Card(
    children=[
        dmc.Text("Pie Chart Card"),
        cornea_utils.get_loading_spinner(landing_zone_cornea_configs.piechart_loading_spinner),
        dmc.CardSection(landing_zone_schema_piechart)
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 550, "height": 500, "margin": "20px"},
)
