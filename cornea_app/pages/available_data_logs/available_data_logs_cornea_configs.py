from cornea_configs import CorneaConfigs


# pylint: disable=R0902, C0103
class AvailableDataLogsCorneaConfigs:
    def __init__(self):
        self.cornea_configs = CorneaConfigs()
        self.available_data_logs_date_range_picker = "available_data_logs_date_range_picker"
        self.available_data_logs_table_select = "available_data_logs_table_select"
        self.available_data_logs_pwk_start_week_text_input = "available_data_logs_pwk_start_week_text_input"
        self.available_data_logs_pwk_end_week_text_input = "available_data_logs_pwk_end_week_text_input"
        self.available_data_logs_output_dataframe = "available_data_logs_output_dataframe"
