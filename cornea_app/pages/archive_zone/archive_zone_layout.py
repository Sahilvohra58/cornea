from dash import html
import dash_mantine_components as dmc

from pages.archive_zone.archive_zone_components.stats_cards_input import stats_cards_input, \
    general_insights_cards
from pages.archive_zone.archive_zone_components.feature_range_explore import feature_range_input, \
    feature_range_explore_card
from pages.archive_zone.archive_zone_components.percentile_box_plot import percentile_input_features_pwk, \
    percentile_plot_card
from pages.archive_zone.archive_zone_cornea_configs import ArchiveZoneCorneaConfigs

archive_zone_cornea_configs = ArchiveZoneCorneaConfigs()

archive_zone_layout = html.Div([
    html.Div(
        [
            stats_cards_input,
            general_insights_cards,
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(children="Avg Values Chart", value=archive_zone_cornea_configs.average_values_card),
                            dmc.Tab(children="Min Values Chart", value=archive_zone_cornea_configs.minimum_values_card),
                            dmc.Tab(children="Max Values Chart", value=archive_zone_cornea_configs.maximum_values_card),
                            dmc.Tab(children="Std Values Chart",
                                    value=archive_zone_cornea_configs.standard_deviation_values_card),
                            dmc.Tab(children="Skew Values Chart", value=archive_zone_cornea_configs.skew_values_card),
                            dmc.Tab(children="Null Values Chart", value=archive_zone_cornea_configs.null_values_card),
                            dmc.Tab(children="Zero Values Chart", value=archive_zone_cornea_configs.zero_values_card),

                        ]
                    ),
                ],
                id=archive_zone_cornea_configs.archive_zone_tabs,
                value=archive_zone_cornea_configs.average_values_card,
                variant="outline"
            ),
            html.Div(id=archive_zone_cornea_configs.archive_zone_tabs_content, style={"paddingTop": 10}),
        ],
        style={"padding": "32px",  # "display": "flex",
               "justifyContent": "space-between"}
    ),
    dmc.Divider(variant="solid"),
    html.Div(
        [
            feature_range_input,
            feature_range_explore_card
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    ),
    dmc.Divider(variant="solid"),
    html.Div(
        [
            percentile_input_features_pwk,
            percentile_plot_card
        ],
        style={"padding": "32px", "display": "flex",
               "justifyContent": "space-between"}
    )
])
