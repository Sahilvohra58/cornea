from datetime import date
import dash_mantine_components as dmc
from dash import html
from google.cloud import firestore

from pages.archive_zone.archive_zone_cornea_configs import ArchiveZoneCorneaConfigs

archive_zone_cornea_configs = ArchiveZoneCorneaConfigs()
firestore_client = firestore.Client(
    project=archive_zone_cornea_configs.cornea_configs.project_id,
    database=archive_zone_cornea_configs.cornea_configs.firestore_database
)

stats_cards_input = dmc.Card(
    children=[
        dmc.TextInput(
            id=archive_zone_cornea_configs.stats_cards_pwk_start_week_text_input,
            label="pwk_start_week",
            description="Format is YYYYWW",
            placeholder="YYYYWW",
            style={"width": 250, "padding": "20px"},
            required=True,
            # value=datetime.now().strftime("%Y%W"),
        ),
        dmc.TextInput(
            id=archive_zone_cornea_configs.stats_cards_pwk_end_week_text_input,
            label="pwk_end_week",
            description="Format is YYYYWW",
            placeholder="YYYYWW",
            style={"width": 250, "padding": "20px"},
            required=True,
            # value=datetime.now().strftime("%Y%W"),
        ),
        dmc.DateRangePicker(
            id=archive_zone_cornea_configs.stats_cards_date_range_picker,
            label="Pick data range (Optional)",
            description="Format is DD/MM/YYYY",
            minDate=date(2020, 8, 5),
            inputFormat="DD/MM/YYYY",
            clearable=True,
            style={"width": 270, "padding": "20px"},
            # required=True,
        ),
        dmc.Select(
            id=archive_zone_cornea_configs.stats_cards_table_select,
            label="Select table id",
            description="All archive zone tables",
            clearable=True,
            data=archive_zone_cornea_configs.cornea_configs.archive_zone_tables,
            value=archive_zone_cornea_configs.cornea_configs.archive_zone_tables[0],
            searchable=True,
            nothingFound="No options found",
            style={"width": 200, "padding": "20px"},
            required=True,
            # py=10,
        ),
        dmc.MultiSelect(
            id=archive_zone_cornea_configs.stats_cards_features_multi_select,
            label="Features (optional)",
            description="If your are looking for specific features.",
            searchable=True,
            clearable=True,
            nothingFound="No options found",
            style={"width": 450, "padding": "20px"},
        ),
        dmc.Divider(orientation="vertical", style={"height": 120}),
        dmc.Select(
            id=archive_zone_cornea_configs.stats_cards_chart_type_select,
            label="Select chart type",
            description="Line or bar chart",
            clearable=False,
            data=["Line chart", "Bar chart"],
            value="Line chart",
            searchable=True,
            # nothingFound="No options found",
            style={"width": 200, "padding": "20px"},
            required=True,
            # py=10,
        ),
        dmc.Switch(
            id=archive_zone_cornea_configs.chart_label_switch,
            radius="sm",
            label="Labels",
            offLabel="off",
            checked=True,
            mt="auto",
            mb="auto",
        ),
        dmc.Button(
            children="Submit",
            variant="outline",
            id=archive_zone_cornea_configs.stats_cards_submit_button,
            ),
    ],
    # py=20,
    px=20,
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"margin": "15px", "display": "flex", "overflow": "visible"},  # "width": 400, "height": 500,
)

total_features_card = dmc.Card(
    children=[
        dmc.Text("Total Features Selected"),
        dmc.Divider(variant="solid"),
        dmc.Text(id=archive_zone_cornea_configs.stats_cards_selected_features, size="50px", weight="300")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 150, "width": 250, "margin": "20px"},
)

total_pwk_records_card = dmc.Card(
    children=[
        dmc.Text("Available PWK Records in the Date Range"),
        dmc.Divider(variant="solid"),
        dmc.Text(id=archive_zone_cornea_configs.stats_cards_available_pwk_records, size="50px", weight="300")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 150, "width": 250, "margin": "20px"},
)

categorical_feature_count_card = dmc.Card(
    children=[
        dmc.Text("Total Categorical Features"),
        dmc.Divider(variant="solid"),
        dmc.Text(id=archive_zone_cornea_configs.stats_cards_categorical_feature_count, size="50px", weight="300")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 150, "width": 250, "margin": "20px"},
)

continuous_feature_count_card = dmc.Card(
    children=[
        dmc.Text("Total Continuous Features"),
        dmc.Divider(variant="solid"),
        dmc.Text(id=archive_zone_cornea_configs.stats_cards_continuous_feature_count, size="50px", weight="300")
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 150, "width": 250, "margin": "20px"},
)

general_insights_cards = html.Div(
    children=[
        total_features_card,
        total_pwk_records_card,
        categorical_feature_count_card,
        continuous_feature_count_card,
        # loading_spinner
    ],
    style={"display": "flex"}
    # "padding": "32px", "justifyContent": "space-between"}
)
