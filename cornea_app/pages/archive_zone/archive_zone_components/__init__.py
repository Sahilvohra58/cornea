from dash import Input, Output, callback, State

from cornea_utils import CorneaUtils
from initialize_cache import cache
from pages.archive_zone.archive_zone_cornea_utils import ArchiveZoneCorneaUtils
from pages.archive_zone.archive_zone_cornea_configs import ArchiveZoneCorneaConfigs


cornea_utils = CorneaUtils()
archive_zone_cornea_configs = ArchiveZoneCorneaConfigs()
archive_zone_cornea_utils = ArchiveZoneCorneaUtils()


@callback(
    Output(archive_zone_cornea_configs.average_values_chart, "figure"),
    Output(archive_zone_cornea_configs.average_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.chart_label_switch, 'checked'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
@cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
def get_average_values_chart(table_id, dates, features, chart_type, chart_label_switch, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(
        metric_type="avg_value", table_id=table_id, dates=dates, features=features,
        chart_type=chart_type, chart_label_switch=chart_label_switch,
        is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.average_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
@cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
def get_average_values_drifts(table_id, dates, features, _):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="avg_value"
    )


@callback(
    Output(archive_zone_cornea_configs.maximum_values_chart, "figure"),
    Output(archive_zone_cornea_configs.maximum_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
@cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
def get_maximum_values_chart(values, dates, features, chart_type, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(metric_type="max_value", table_id=values, dates=dates, features=features,
                                              chart_type=chart_type, is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.maximum_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),

)
def get_maximum_values_drifts(table_id, dates, features, _):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="max_value"
    )


@callback(
    Output(archive_zone_cornea_configs.minimum_values_chart, "figure"),
    Output(archive_zone_cornea_configs.minimum_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_minimum_values_chart(values, dates, features, chart_type, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(
        metric_type="min_value", table_id=values, dates=dates, features=features,
        chart_type=chart_type, is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.minimum_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_minimum_values_drifts(table_id, dates, features, _):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="min_value"
    )


@callback(
    Output(archive_zone_cornea_configs.null_values_chart, "figure"),
    Output(archive_zone_cornea_configs.null_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_null_values_chart(values, dates, features, chart_type, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(
        metric_type="null_count", table_id=values, dates=dates, features=features,
        chart_type=chart_type, is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.null_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_null_values_drifts(table_id, dates, features):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="null_count"
    )


@callback(
    Output(archive_zone_cornea_configs.skew_values_chart, "figure"),
    Output(archive_zone_cornea_configs.skew_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_skew_values_chart(values, dates, features, chart_type, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(
        metric_type="skew", table_id=values, dates=dates, features=features,
        chart_type=chart_type, is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.skew_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_skew_values_drifts(table_id, dates, features, _):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="skew"
    )


@callback(
    Output(archive_zone_cornea_configs.standard_deviation_values_chart, "figure"),
    Output(archive_zone_cornea_configs.standard_deviation_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_standard_deviation_chart(values, dates, features, chart_type, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(
        metric_type="std_value", table_id=values, dates=dates, features=features,
        chart_type=chart_type, is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.standard_deviation_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_standard_deviation_values_drifts(table_id, dates, features, _):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="std_value"
    )


@callback(
    Output(archive_zone_cornea_configs.zero_values_chart, "figure"),
    Output(archive_zone_cornea_configs.zero_values_loading_spinner, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_zero_values_chart(values, dates, features, chart_type, is_light_mode, _):
    fig = archive_zone_cornea_utils.get_chart(metric_type="zero_count", table_id=values, dates=dates, features=features,
                                              chart_type=chart_type, is_light_mode=is_light_mode)
    return fig, None


@callback(
    Output(archive_zone_cornea_configs.zero_values_feature_drifts, "children"),
    State(archive_zone_cornea_configs.stats_cards_table_select, "value"),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_zero_values_drifts(table_id, dates, features, _):
    return archive_zone_cornea_utils.get_drifts_content(
        table_id=table_id,
        dates=dates,
        features=features,
        metric_type="zero_count"
    )


@callback(
    Output(archive_zone_cornea_configs.feature_range_feature_multi_select, 'data'),
    Output(archive_zone_cornea_configs.feature_range_feature_multi_select, 'value'),
    Input(archive_zone_cornea_configs.feature_range_table_select, 'value')
)
def update_feature_list_dropdown(table_id):
    features_list = archive_zone_cornea_utils.get_features_list(table_id=table_id)
    return features_list, features_list[0:1]


@callback(
    Output(archive_zone_cornea_configs.feature_range_explore_chart, 'figure'),
    Input(archive_zone_cornea_configs.feature_range_table_select, "value"),
    Input(archive_zone_cornea_configs.feature_range_date_range_picker, 'value'),
    Input(archive_zone_cornea_configs.feature_range_feature_multi_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked')
)
def get_range_plot(table_id, dates, features=None, is_light_mode=None):
    return archive_zone_cornea_utils.get_range_plot_content(
        table_id=table_id,
        dates=dates,
        features=features,
        is_light_mode=is_light_mode
    )


@callback(
    Output(archive_zone_cornea_configs.percentile_feature_multi_select, 'data'),
    Output(archive_zone_cornea_configs.percentile_feature_multi_select, 'value'),
    Input(archive_zone_cornea_configs.percentile_feature_table_select, 'value')
)
def update_pwk_feature_list_dropdown(table_id):
    features_list = archive_zone_cornea_utils.get_features_list(table_id=table_id)
    return features_list, features_list[0:1]


@callback(
    Output(archive_zone_cornea_configs.percentile_box_plot_chart, 'figure'),
    Input(archive_zone_cornea_configs.percentile_input_pwk, "value"),
    Input(archive_zone_cornea_configs.percentile_feature_table_select, 'value'),
    Input(archive_zone_cornea_configs.percentile_feature_multi_select, 'value'),
    Input(archive_zone_cornea_configs.percentile_chart_type_select, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.theme_switch, 'checked')
)
def get_percentile_box_plot(pwk_week, table_id, features=None, chart_type="Box Plot", is_light_mode=None):
    return archive_zone_cornea_utils.get_percentile_box_plot_content(
        pwk_week=pwk_week,
        table_id=table_id,
        features=features,
        chart_type=chart_type,
        is_light_mode=is_light_mode
    )


@callback(
    Output(archive_zone_cornea_configs.stats_cards_pwk_start_week_text_input, 'error'),
    Output(archive_zone_cornea_configs.stats_cards_pwk_end_week_text_input, 'error'),
    Input(archive_zone_cornea_configs.stats_cards_pwk_start_week_text_input, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_pwk_end_week_text_input, 'value')
)
def update_start_week_error_text(text_start, text_end):
    return cornea_utils.week_pwk_format_error_text(text_start=text_start, text_end=text_end)


@callback(
    Output(archive_zone_cornea_configs.stats_cards_features_multi_select, 'data'),
    Input(archive_zone_cornea_configs.stats_cards_table_select, 'value')
)
def update_date_dropdown(table_id):
    return archive_zone_cornea_utils.get_features_list(table_id=table_id)


@callback(
    Output(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_pwk_start_week_text_input, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_pwk_end_week_text_input, 'value')
)
def update_date_picker_from_pwk(start_pwk, end_pwk):
    return cornea_utils.date_picker_from_pwk(start_pwk=start_pwk, end_pwk=end_pwk)


@callback(
    Output(archive_zone_cornea_configs.stats_cards_date_range_picker, 'error'),
    Input(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
)
def update_date_picker_error_text(dates):
    return cornea_utils.date_picker_error_text(dates=dates)


@callback(
    Output(archive_zone_cornea_configs.stats_cards_pwk_start_week_text_input, 'value'),
    Output(archive_zone_cornea_configs.stats_cards_pwk_end_week_text_input, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.global_pwk_start_week_text_input, 'value'),
    Input(archive_zone_cornea_configs.cornea_configs.global_pwk_end_week_text_input, 'value')
)
def update_pwk_from_global_pwk_archive_zone(start_pwk, end_pwk):
    return start_pwk, end_pwk


@callback(
    Output(archive_zone_cornea_configs.stats_cards_selected_features, 'children'),
    Input(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    State(archive_zone_cornea_configs.stats_cards_table_select, 'value'),
    State(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def get_total_selected_features_count(selected_features, table_id, dates, _):
    return archive_zone_cornea_utils.total_selected_features_count(
        selected_features=selected_features,
        table_id=table_id,
        dates=dates)


@callback(
    Output(archive_zone_cornea_configs.stats_cards_available_pwk_records, 'children'),
    Input(archive_zone_cornea_configs.stats_cards_date_range_picker, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_table_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),

)
def update_pwk_records_card(dates, table_id, _):
    return archive_zone_cornea_utils.pwk_records_card_content(dates=dates, table_id=table_id)


@callback(
    Output(archive_zone_cornea_configs.stats_cards_categorical_feature_count, 'children'),
    Output(archive_zone_cornea_configs.stats_cards_continuous_feature_count, 'children'),
    State(archive_zone_cornea_configs.stats_cards_table_select, 'value'),
    State(archive_zone_cornea_configs.stats_cards_features_multi_select, 'value'),
    Input(archive_zone_cornea_configs.stats_cards_submit_button, "n_clicks"),
)
def update_feature_type_cards(table_id, features, _):
    return archive_zone_cornea_utils.feature_type_cards_content(table_id=table_id, features=features)


@callback(
    Output(archive_zone_cornea_configs.archive_zone_tabs_content, "children"),
    Input(archive_zone_cornea_configs.archive_zone_tabs, "value")
)
def render_content(active):
    return archive_zone_cornea_utils.render_archive_zone_content(active=active)
