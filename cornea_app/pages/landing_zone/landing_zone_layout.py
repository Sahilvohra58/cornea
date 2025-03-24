from dash import html
import dash_mantine_components as dmc

from pages.landing_zone.landing_zone_components.input_card import landing_zone_input
from pages.landing_zone.landing_zone_cornea_configs import LandingZoneCorneaConfigs

landing_zone_cornea_configs = LandingZoneCorneaConfigs()

landing_zone_layout = html.Div([
    html.Div(
        [
            landing_zone_input,
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(children="Row Count Chart", value=landing_zone_cornea_configs.row_count_card),
                            dmc.Tab(children="Null Count Chart", value=landing_zone_cornea_configs.null_count_card),
                            dmc.Tab(children="Min Values Chart", value=landing_zone_cornea_configs.min_values_card),
                            dmc.Tab(children="Max Values Chart", value=landing_zone_cornea_configs.max_values_card),
                            dmc.Tab(children="Other Charts", value=landing_zone_cornea_configs.other_charts),

                        ]
                    ),
                ],
                id=landing_zone_cornea_configs.landing_zone_tabs,
                value=landing_zone_cornea_configs.row_count_card,
                variant="outline"
            ),
            html.Div(id=landing_zone_cornea_configs.landing_zone_tabs_content, style={"paddingTop": 10}),
        ],
        style={"padding": "32px",  # "display": "flex",
               "justifyContent": "space-between"}
    ),
    dmc.Divider(variant="solid"),
])
