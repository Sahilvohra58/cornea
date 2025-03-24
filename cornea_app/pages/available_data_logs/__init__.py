import pandas as pd
from dash import Input, Output, callback
from google.cloud import firestore

from cornea_utils import CorneaUtils
from pages.available_data_logs.available_data_logs_cornea_configs import AvailableDataLogsCorneaConfigs
from initialize_cache import cache


cornea_utils = CorneaUtils()
available_data_logs_cornea_configs = AvailableDataLogsCorneaConfigs()
firestore_client = firestore.Client(
    project=available_data_logs_cornea_configs.cornea_configs.project_id,
    database=available_data_logs_cornea_configs.cornea_configs.firestore_database
)


@callback(
    Output(available_data_logs_cornea_configs.available_data_logs_output_dataframe, "data"),
    Output(available_data_logs_cornea_configs.available_data_logs_output_dataframe, "columns"),
    Input(available_data_logs_cornea_configs.available_data_logs_date_range_picker, "value"),
    Input(available_data_logs_cornea_configs.available_data_logs_table_select, "value")
)
@cache.memoize(timeout=available_data_logs_cornea_configs.cornea_configs.cache_timeout)
def get_all_dates_list(dates, table_id):
    initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
    date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
    date_exists_list = []
    for date_str in date_range:
        collection = firestore_client.collection(f"archive_zone/{table_id}/{date_str}")
        if len(list(collection.list_documents())) > 0:
            date_exists_list.append(date_str)
    df = pd.DataFrame(date_exists_list, columns=[table_id])
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


@callback(
    Output(available_data_logs_cornea_configs.available_data_logs_pwk_start_week_text_input, 'error'),
    Output(available_data_logs_cornea_configs.available_data_logs_pwk_end_week_text_input, 'error'),
    Input(available_data_logs_cornea_configs.available_data_logs_pwk_start_week_text_input, 'value'),
    Input(available_data_logs_cornea_configs.available_data_logs_pwk_end_week_text_input, 'value')
)
@cache.memoize(timeout=available_data_logs_cornea_configs.cornea_configs.cache_timeout)
def update_start_week_error_text_available_data(text_start, text_end):
    return cornea_utils.week_pwk_format_error_text(text_start=text_start, text_end=text_end)


@callback(
    Output(available_data_logs_cornea_configs.available_data_logs_date_range_picker, 'value'),
    Input(available_data_logs_cornea_configs.available_data_logs_pwk_start_week_text_input, 'value'),
    Input(available_data_logs_cornea_configs.available_data_logs_pwk_end_week_text_input, 'value')
)
@cache.memoize(timeout=available_data_logs_cornea_configs.cornea_configs.cache_timeout)
def update_date_picker_from_pwk_available_data(start_pwk, end_pwk):
    return cornea_utils.date_picker_from_pwk(start_pwk=start_pwk, end_pwk=end_pwk)
