import os

env = os.getenv('ENV', 'exp')


# pylint: disable=R0902
class CorneaConfigs:
    def __init__(self):
        self.app_title = "Cornea"
        self.app_theme_id = "app_theme_id"
        self.project_id = f"lt-dia-analytics-{env}-ptp"
        self.firestore_database = "cornea"
        self.theme_switch = "switch-theme"
        self.tabs_list_id = "tabs_list_id"
        self.tabs_content_id = "tabs_content_id"
        self.cache_timeout = 60
        self.cornea_credentials_key = "cornea_username_password_pairs"

        self.global_pwk_start_week_text_input = "global_pwk_start_week_text_input"
        self.global_pwk_end_week_text_input = "global_pwk_end_week_text_input"

        self.archive_zone_tables = [
            "CID_WK_CAT", "CID_MT_ATR", "CID_MT_BEH", "CID_MT_CAT", "CID_WK_BEH",
            "CID_MT_INT", "CID_MT_OFF", "CID_WK_INT", "CID_WK_OFF"
        ]

        self.dag_runs_tab_id = "dag_runs_tab_id"
        self.archive_zone_tab_id = "archive_zone_tab_id"
        self.landing_zone_tab_id = "landing_zone_tab_id"
        self.available_data_logs_tab_id = "available_data_logs_tab_id"
