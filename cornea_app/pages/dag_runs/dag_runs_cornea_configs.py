from cornea_configs import CorneaConfigs


class DagRunsCorneaConfigs:
    def __init__(self):
        self.cornea_configs = CorneaConfigs()
        self.dag_runs_chart_type_switch = "dag_runs_chart_type_switch"
        self.dag_runs_date_range_picker = "dag_runs_date_range_picker"
        self.dag_runs_zone_checklist = "dag_runs_zone_checklist"
        self.dag_runs_chart = "dag_runs_chart"
        self.dag_runs_all_zones = ["landing_zone", "transform_hub", "scoring_engine", "archive_hub", "archive_zone",
                                   "trend_hub", "trend_zone", "config_zone", "reference_hub", "others"]
        self.dag_runs_all_zones_defaults = ["landing_zone", "transform_hub", "scoring_engine", "archive_hub",
                                            "archive_zone", "trend_hub", "trend_zone"]
