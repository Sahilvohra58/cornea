from dash import Input, Output, callback, State

from initialize_cache import cache
from pages.landing_zone.landing_zone_cornea_configs import LandingZoneCorneaConfigs
from pages.landing_zone.landing_zone_cornea_utils import LandingZoneCorneaUtils

from cornea_utils import CorneaUtils

landing_zone_cornea_configs = LandingZoneCorneaConfigs()
landing_zone_cornea_utils = LandingZoneCorneaUtils()
cornea_utils = CorneaUtils()


@callback(
    Output(landing_zone_cornea_configs.landing_zone_pwk_start_week_text_input, 'error'),
    Output(landing_zone_cornea_configs.landing_zone_pwk_end_week_text_input, 'error'),
    Input(landing_zone_cornea_configs.landing_zone_pwk_start_week_text_input, 'value'),
    Input(landing_zone_cornea_configs.landing_zone_pwk_end_week_text_input, 'value')

)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def update_start_week_error_text_landing_zone(text_start, text_end):
    return cornea_utils.week_pwk_format_error_text(text_start=text_start, text_end=text_end)


@callback(
    Output(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
    Input(landing_zone_cornea_configs.landing_zone_pwk_start_week_text_input, 'value'),
    Input(landing_zone_cornea_configs.landing_zone_pwk_end_week_text_input, 'value')
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def update_date_picker_from_pwk_landing_zone(start_pwk, end_pwk):
    return cornea_utils.date_picker_from_pwk(start_pwk=start_pwk, end_pwk=end_pwk)


@callback(
    Output(landing_zone_cornea_configs.landing_zone_date_range_picker, 'error'),
    Input(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def update_date_picker_error_text(dates):
    return cornea_utils.date_picker_error_text(dates=dates)


@callback(
    Output(landing_zone_cornea_configs.landing_zone_input_table_features_select, 'data'),
    Input(landing_zone_cornea_configs.landing_zone_table_select, 'value')
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def update_date_dropdown(table_id):
    return landing_zone_cornea_utils.get_features_list(table_id=table_id)


@callback(
    Output(landing_zone_cornea_configs.landing_zone_pwk_start_week_text_input, 'value'),
    Output(landing_zone_cornea_configs.landing_zone_pwk_end_week_text_input, 'value'),
    Input(landing_zone_cornea_configs.cornea_configs.global_pwk_start_week_text_input, 'value'),
    Input(landing_zone_cornea_configs.cornea_configs.global_pwk_end_week_text_input, 'value')
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def update_pwk_from_global_pwk_landing_zone(start_pwk, end_pwk):
    return start_pwk, end_pwk


@callback(
    Output(landing_zone_cornea_configs.max_values_chart, "figure"),
    Output(landing_zone_cornea_configs.max_values_min_values_card, "children"),
    Output(landing_zone_cornea_configs.max_values_max_values_card, "children"),
    Output(landing_zone_cornea_configs.max_values_drift_card, "children"),
    Output(landing_zone_cornea_configs.max_values_loading_spinner, "children"),

    State(landing_zone_cornea_configs.landing_zone_table_select, "value"),
    State(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
    State(landing_zone_cornea_configs.landing_zone_input_table_features_select, "value"),

    Input(landing_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(landing_zone_cornea_configs.landing_zone_submit_button, "n_clicks"),
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def get_max_values_chart(landing_id, dates, features, is_light_mode, _):
    return landing_zone_cornea_utils.get_min_max_values_chart(
        landing_id=landing_id,
        dates=dates,
        features=features,
        is_light_mode=is_light_mode,
        metric_type="max_values_count")


@callback(
    Output(landing_zone_cornea_configs.min_values_chart, "figure"),
    Output(landing_zone_cornea_configs.min_values_min_values_card, "children"),
    Output(landing_zone_cornea_configs.min_values_max_values_card, "children"),
    Output(landing_zone_cornea_configs.min_values_drift_card, "children"),
    Output(landing_zone_cornea_configs.min_values_loading_spinner, "children"),

    State(landing_zone_cornea_configs.landing_zone_table_select, "value"),
    State(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
    State(landing_zone_cornea_configs.landing_zone_input_table_features_select, "value"),

    Input(landing_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(landing_zone_cornea_configs.landing_zone_submit_button, "n_clicks"),
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def get_min_values_chart(landing_id, dates, features, is_light_mode, _):
    return landing_zone_cornea_utils.get_min_max_values_chart(
        landing_id=landing_id,
        dates=dates,
        features=features,
        is_light_mode=is_light_mode,
        metric_type="min_values_count")


@callback(
    Output(landing_zone_cornea_configs.null_count_chart, "figure"),
    Output(landing_zone_cornea_configs.null_count_total_columns, "children"),

    Output(landing_zone_cornea_configs.null_count_all_feature_min_value, "children"),
    Output(landing_zone_cornea_configs.null_count_all_feature_max_value, "children"),

    Output(landing_zone_cornea_configs.null_count_min_values_card, "children"),
    Output(landing_zone_cornea_configs.null_count_max_values_card, "children"),

    Output(landing_zone_cornea_configs.null_count_drift_card, "children"),

    Output(landing_zone_cornea_configs.null_count_loading_spinner, "children"),

    State(landing_zone_cornea_configs.landing_zone_table_select, "value"),
    State(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
    State(landing_zone_cornea_configs.landing_zone_input_table_features_select, "value"),

    Input(landing_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(landing_zone_cornea_configs.landing_zone_submit_button, "n_clicks"),

)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def get_null_count_chart(landing_id, dates, features, is_light_mode, _):
    return landing_zone_cornea_utils.get_null_count_chart(landing_id, dates, features, is_light_mode)


@callback(
    Output(landing_zone_cornea_configs.landing_zone_schema_piechart, "figure"),
    Output(landing_zone_cornea_configs.piechart_loading_spinner, "children"),
    State(landing_zone_cornea_configs.landing_zone_table_select, "value"),
    State(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
    Input(landing_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(landing_zone_cornea_configs.landing_zone_submit_button, "n_clicks"),
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def generate_pie_chart(landing_id, dates, is_light_mode, _):
    return landing_zone_cornea_utils.generate_pie_chart(
        landing_id=landing_id,
        dates=dates,
        is_light_mode=is_light_mode
    )


@callback(
    Output(landing_zone_cornea_configs.row_count_chart, "figure"),
    Output(landing_zone_cornea_configs.row_count_total_records, "children"),
    Output(landing_zone_cornea_configs.row_count_min_value, "children"),
    Output(landing_zone_cornea_configs.row_count_max_value, "children"),
    Output(landing_zone_cornea_configs.row_count_loading_spinner, "children"),
    State(landing_zone_cornea_configs.landing_zone_table_select, "value"),
    State(landing_zone_cornea_configs.landing_zone_date_range_picker, 'value'),
    Input(landing_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(landing_zone_cornea_configs.landing_zone_submit_button, "n_clicks"),
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def get_row_count_chart_and_insights(landing_id, dates, is_light_mode, _):
    return landing_zone_cornea_utils.get_row_count_chart_and_insights(
        landing_id=landing_id,
        dates=dates,
        is_light_mode=is_light_mode
    )


@callback(
    Output(landing_zone_cornea_configs.landing_zone_tabs_content, "children"),
    Input(landing_zone_cornea_configs.landing_zone_tabs, "value")
)
@cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
def render_content(active):
    return landing_zone_cornea_utils.render_landing_zone_content(active=active)
