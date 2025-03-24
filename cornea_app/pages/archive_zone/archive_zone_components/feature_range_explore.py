from datetime import datetime, timedelta, date
import dash_mantine_components as dmc
from dash import dcc
from google.cloud import firestore

from pages.archive_zone.archive_zone_cornea_configs import ArchiveZoneCorneaConfigs
from cornea_utils import CorneaUtils

cornea_utils = CorneaUtils()
archive_zone_cornea_configs = ArchiveZoneCorneaConfigs()
firestore_client = firestore.Client(
    project=archive_zone_cornea_configs.cornea_configs.project_id,
    database=archive_zone_cornea_configs.cornea_configs.firestore_database
)


feature_range_input = dmc.Card(
    children=[
        dmc.Text("For exploring individual features"),
        dmc.DateRangePicker(
            id=archive_zone_cornea_configs.feature_range_date_range_picker,
            label="Pick your data range",
            description="The date range for the archive zone data",
            minDate=date(2020, 8, 5),
            # inputFormat="DD-MM-YYYY",
            clearable=True,
            value=[datetime.now().date() - timedelta(days=7), datetime.now().date()],
            style={"width": 350, "padding": "20px"},
            required=True,
        ),
        dmc.Select(
            id=archive_zone_cornea_configs.feature_range_table_select,
            label="Select the table type",
            description="This has a list of all archive zone tables",
            clearable=True,
            data=archive_zone_cornea_configs.cornea_configs.archive_zone_tables,
            value=archive_zone_cornea_configs.cornea_configs.archive_zone_tables[0],
            searchable=True,
            nothingFound="No options found",
            style={"width": 330, "padding": "20px"},
            required=True,
            # py=10,
        ),
        dmc.Select(
            id=archive_zone_cornea_configs.feature_range_feature_multi_select,
            label="Features (max 1)",
            description="If your are looking for specific features.",
            searchable=True,
            clearable=True,
            nothingFound="No options found",
            required=True,
            style={"width": 350, "padding": "20px"},
        )
    ],
    # py=20,
    px=20,
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"margin": "15px", "width": 400, "height": 500, "overflow": "visible"},
)


feature_range_explore_chart = dcc.Graph(
    id=archive_zone_cornea_configs.feature_range_explore_chart,
    style={"padding": "20px", "overflowY": "scroll", "overflowX": "scroll"}
)

feature_range_explore_card = dmc.Card(
    children=[
        dmc.Text("Feature exploration Chart"),
        cornea_utils.get_loading_spinner(archive_zone_cornea_configs.feature_range_loading_spinner),
        dmc.CardSection(feature_range_explore_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 500, "width": 1200, "margin": "20px", "overflowY": "scroll", "overflowX": "scroll"},
)
