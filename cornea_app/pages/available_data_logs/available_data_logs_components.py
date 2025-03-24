from datetime import datetime, date, timedelta
from google.cloud import firestore
from dash import dash_table
import dash_mantine_components as dmc

from pages.available_data_logs.available_data_logs_cornea_configs import AvailableDataLogsCorneaConfigs

available_data_logs_cornea_configs = AvailableDataLogsCorneaConfigs()
firestore_client = firestore.Client(
    project=available_data_logs_cornea_configs.cornea_configs.project_id,
    database=available_data_logs_cornea_configs.cornea_configs.firestore_database
)

available_data_input = dmc.Card(
    children=[
        dmc.DateRangePicker(
            id=available_data_logs_cornea_configs.available_data_logs_date_range_picker,
            label="Pick your data range",
            description="Format is DD/MM/YYYY",
            minDate=date(2020, 8, 5),
            inputFormat="DD/MM/YYYY",
            clearable=True,
            value=[datetime.now().date() - timedelta(days=100), datetime.now().date()],
            style={"width": 350, "padding": "20px"},
            required=True,
        ),
        dmc.Select(
            id=available_data_logs_cornea_configs.available_data_logs_table_select,
            label="Select table id",
            description="All archive zone tables",
            clearable=True,
            data=available_data_logs_cornea_configs.cornea_configs.archive_zone_tables,
            value=available_data_logs_cornea_configs.cornea_configs.archive_zone_tables[0],
            searchable=True,
            nothingFound="No options found",
            style={"width": 200, "padding": "20px"},
            required=True,
            # py=10,
        ),
        dmc.Divider(orientation="vertical", style={"height": 120}),
        dmc.TextInput(
            id=available_data_logs_cornea_configs.available_data_logs_pwk_start_week_text_input,
            label="pwk_start_week (Optional)",
            description="Query data by pwk instead of dates.",
            placeholder="YYYYWW",
            style={"width": 280, "padding": "20px"}
        ),
        dmc.TextInput(
            id=available_data_logs_cornea_configs.available_data_logs_pwk_end_week_text_input,
            label="pwk_end_week (Optional)",
            description="Query data by pwk instead of dates.",
            placeholder="YYYYWW",
            style={"width": 280, "padding": "20px"}
        ),
    ],
    # py=20,
    px=20,
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"margin": "15px", "display": "flex", "overflow": "visible"},  # "width": 400, "height": 500,
)

available_data_page_layout = dash_table.DataTable(
    id=available_data_logs_cornea_configs.available_data_logs_output_dataframe
)
