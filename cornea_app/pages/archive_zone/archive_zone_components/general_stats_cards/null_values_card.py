import dash_mantine_components as dmc
from dash import dcc, html

from pages.archive_zone.archive_zone_cornea_configs import ArchiveZoneCorneaConfigs
from cornea_utils import CorneaUtils

cornea_utils = CorneaUtils()
archive_zone_cornea_configs = ArchiveZoneCorneaConfigs()

null_values_chart = dcc.Graph(id=archive_zone_cornea_configs.null_values_chart,
                              style={"padding": "20px"})

null_values_card = dmc.Card(
    children=[
        dmc.Text("Null Count Chart"),
        cornea_utils.get_loading_spinner(archive_zone_cornea_configs.null_values_loading_spinner),
        dmc.CardSection(null_values_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 500, "width": 1300, "margin": "20px"},
)


null_values_drift_card = dmc.Card(
    children=[
        dmc.Text("Drift in Null Values For Selected Features"),
        dmc.Divider(variant="solid"),
        html.Div(id=archive_zone_cornea_configs.null_values_feature_drifts, style={"paddingTop": 10}),

    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 500, "height": 500, "margin": "20px", 'overflow': 'scroll'},
)
