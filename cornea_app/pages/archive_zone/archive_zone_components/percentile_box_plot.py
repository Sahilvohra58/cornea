from datetime import datetime, timedelta
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

percentile_input_features_pwk = dmc.Card(
    children=[
        dmc.Text("For exploring individual features for specific PWKs"),
        dmc.Select(
            id=archive_zone_cornea_configs.percentile_chart_type_select,
            description="Choose either Box plot or Bar chart",
            value="Box Plot",
            data=["Box Plot", "Percentile Bar Chart", "Histogram"],
            searchable=True,
            clearable=True,
            nothingFound="No options found",
            required=True,
            style={"width": 350, "padding": "10px"},
        ),
        dmc.TextInput(
            id=archive_zone_cornea_configs.percentile_input_pwk,
            label="PWK week",
            value=datetime.strftime(datetime.today() - timedelta(days=(datetime.today().weekday() - 3) % 7), "%Y%W"),
            description="Query data by pwk",
            placeholder="YYYYWW",
            style={"width": 280, "padding": "10px"}
        ),
        dmc.Select(
            id=archive_zone_cornea_configs.percentile_feature_table_select,
            label="Select the table type",
            description="This has a list of all archive zone tables",
            clearable=True,
            data=archive_zone_cornea_configs.cornea_configs.archive_zone_tables,
            value=archive_zone_cornea_configs.cornea_configs.archive_zone_tables[0],
            searchable=True,
            nothingFound="No options found",
            style={"width": 330, "padding": "10px"},
            required=True,
            # py=10,
        ),
        dmc.MultiSelect(
            id=archive_zone_cornea_configs.percentile_feature_multi_select,
            label="Features (max 3)",
            maxSelectedValues=3,
            description="If your are looking for specific features.",
            searchable=True,
            clearable=True,
            nothingFound="No options found",
            required=True,
            style={"width": 350, "padding": "10px"},
        )
    ],
    # py=20,
    px=20,
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"margin": "15px", "width": 400, "height": 550, "overflow": "visible"},
)

percentile_plot_chart = dcc.Graph(id=archive_zone_cornea_configs.percentile_box_plot_chart, style={"padding": "20px"})

percentile_plot_card = dmc.Card(
    children=[
        dmc.Text("Plot Chart"),
        cornea_utils.get_loading_spinner(archive_zone_cornea_configs.percentile_plot_loading_spinner),
        dmc.CardSection(percentile_plot_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 550, "width": 1200, "margin": "20px"},
)
