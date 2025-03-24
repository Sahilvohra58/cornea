from datetime import date
import dash_mantine_components as dmc

from pages.landing_zone.landing_zone_cornea_configs import LandingZoneCorneaConfigs

landing_zone_cornea_configs = LandingZoneCorneaConfigs()

landing_zone_input = dmc.Card(
    children=[
        dmc.TextInput(
            id=landing_zone_cornea_configs.landing_zone_pwk_start_week_text_input,
            label="pwk_start_week",
            description="Query data by pwk.",
            required=True,
            placeholder="YYYYWW",
            py=10,
            style={"width": 120},  # "padding": "20px"}
            # value=datetime.now().strftime("%Y%W"),
        ),
        dmc.TextInput(
            id=landing_zone_cornea_configs.landing_zone_pwk_end_week_text_input,
            label="pwk_end_week",
            description="Query data by pwk.",
            required=True,
            placeholder="YYYYWW",
            py=10,
            style={"width": 120},  # "padding": "20px"}
            # value=datetime.now().strftime("%Y%W"),
        ),
        dmc.Divider(variant="solid"),
        dmc.DateRangePicker(
            id=landing_zone_cornea_configs.landing_zone_date_range_picker,
            label="Pick your data range (Optional)",
            description="The date range for the landing zone data",
            minDate=date(2020, 8, 5),
            # inputFormat="DD-MM-YYYY",
            clearable=True,
            # value=[datetime.now().date() - timedelta(days=7), datetime.now().date()],
            style={"width": 330},
            required=True,
            py=10
        ),
        dmc.Select(
            id=landing_zone_cornea_configs.landing_zone_table_select,
            label="Select the landing ID type",
            description="This has a list of all landing IDs",
            clearable=True,
            data=landing_zone_cornea_configs.landing_zone_tables,
            value=landing_zone_cornea_configs.landing_zone_tables[0],
            searchable=True,
            nothingFound="No options found",
            style={"width": 330},
            required=True,
            py=10,
        ),
        dmc.MultiSelect(
            id=landing_zone_cornea_configs.landing_zone_input_table_features_select,
            label="Features (optional)",
            description="If your are looking for specific features.",
            searchable=True,
            clearable=True,
            nothingFound="No options found",
            style={"width": 450, "padding": "20px"},
        ),
        dmc.Button(
            children="Submit",
            variant="outline",
            id=landing_zone_cornea_configs.landing_zone_submit_button,
            ),

    ],
    # py=20,
    px=20,
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"margin": "15px", "display": "flex", "overflow": "visible", "justify-content": "space-between"},
)
