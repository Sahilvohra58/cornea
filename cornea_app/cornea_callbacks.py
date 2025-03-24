import dash_mantine_components as dmc
from dash import Output, Input, callback

from initialize_cache import cache
from pages.dag_runs.dag_runs_layout import dag_runs_layout
from pages.landing_zone.landing_zone_layout import landing_zone_layout
from pages.archive_zone.archive_zone_layout import archive_zone_layout
from pages.available_data_logs.available_data_logs_layout import available_data_layout
from cornea_configs import CorneaConfigs
from cornea_utils import CorneaUtils


cornea_configs = CorneaConfigs()
cornea_utils = CorneaUtils()


@callback(
    Output(cornea_configs.tabs_content_id, "children"),
    Input(cornea_configs.tabs_list_id, "value")
)
@cache.memoize(timeout=cornea_configs.cache_timeout)
def render_content(active):
    if active == cornea_configs.dag_runs_tab_id:
        return [dag_runs_layout]
    elif active == cornea_configs.landing_zone_tab_id:
        return [landing_zone_layout]
    elif active == cornea_configs.archive_zone_tab_id:
        return [archive_zone_layout]
    elif active == cornea_configs.available_data_logs_tab_id:
        return [available_data_layout]
    else:
        return [dmc.Text("Wrong Tab Selected")]


@callback(
    Output(cornea_configs.app_theme_id, 'theme'),
    Input(cornea_configs.app_theme_id, 'theme'),
    Input(cornea_configs.theme_switch, "checked"),
    prevent_intial_call=True)
@cache.memoize(timeout=cornea_configs.cache_timeout)
def switch_theme(theme, checked):
    if not checked:
        theme.update({'colorScheme': 'dark'})
    else:
        theme.update({'colorScheme': 'white'})
    return theme


@callback(
    Output(cornea_configs.global_pwk_start_week_text_input, 'error'),
    Output(cornea_configs.global_pwk_end_week_text_input, 'error'),
    Input(cornea_configs.global_pwk_start_week_text_input, 'value'),
    Input(cornea_configs.global_pwk_end_week_text_input, 'value')

)
@cache.memoize(timeout=cornea_configs.cache_timeout)
def update_start_week_error_text_global(text_start, text_end):
    return cornea_utils.week_pwk_format_error_text(text_start=text_start, text_end=text_end)
