from cornea_configs import CorneaConfigs


# pylint: disable=R0902
class LandingZoneCorneaConfigs:
    def __init__(self):
        self.cornea_configs = CorneaConfigs()

        self.row_count_card = "row_count_card"
        self.row_count_chart = "row_count_chart"
        self.row_count_total_records = "row_count_total_records"
        self.row_count_min_value = "row_count_min_value"
        self.row_count_max_value = "row_count_max_value"
        self.row_count_loading_spinner = "row_count_loading_spinner"

        self.null_count_card = "null_count_card"
        self.null_count_chart = "null_count_chart"
        self.null_count_total_columns = "null_count_total_columns"
        self.null_count_all_feature_min_value = "null_count_all_feature_min_value"
        self.null_count_all_feature_max_value = "null_count_all_feature_max_value"
        self.null_count_loading_spinner = "null_count_loading_spinner"
        self.null_count_min_values_card = "null_count_min_values_card"
        self.null_count_max_values_card = "null_count_max_values_card"
        self.null_count_drift_card = "null_count_drift_card"

        self.min_values_card = "min_values_card"
        self.min_values_chart = "min_values_chart"
        self.min_values_loading_spinner = "min_values_loading_spinner"
        self.min_values_min_values_card = "min_values_min_values_card"
        self.min_values_max_values_card = "min_values_max_values_card"
        self.min_values_drift_card = "min_values_drift_card"

        self.max_values_card = "max_values_card"
        self.max_values_chart = "max_values_chart"
        self.max_values_loading_spinner = "max_values_loading_spinner"
        self.max_values_min_values_card = "max_values_min_values_card"
        self.max_values_max_values_card = "max_values_max_values_card"
        self.max_values_drift_card = "max_values_drift_card"

        self.other_charts = "other_charts"
        self.landing_zone_schema_piechart = "landing_zone_schema_piechart"
        self.piechart_loading_spinner = "piechart_loading_spinner"

        self.landing_zone_tabs = "landing_zone_tabs"
        self.landing_zone_tabs_content = "landing_zone_tabs_content"

        self.landing_zone_tables = [
            'grocery_behavior_wk', 'ent_sales_wk', 'offer_attributes_mt', 'pco_data_mt', 'promo_sdm_sales',
            'sdm_behavior_wk', 'backfill_grocery_product', 'backfill_offer_behavior', 'backfill_pccat_sales',
            'backfill_landing_promo_sdm_sales', 'backfill_offer_attributes', 'backfill_grocery_behavior',
            'backfill_pco_data', 'backfill_grocery_sales', 'backfill_promo_lcl_sales', 'backfill_ent_sales',
            'backfill_sdm_product', 'offer_behavior_wk'
        ]

        self.landing_zone_table_select = "landing_zone_table_select"
        self.landing_zone_input_table_features_select = "landing_zone_input_table_features_select"
        self.landing_zone_date_range_picker = "landing_zone_date_range_picker"

        self.landing_zone_pwk_start_week_text_input = "landing_zone_pwk_start_week_text_input"
        self.landing_zone_pwk_end_week_text_input = "landing_zone_pwk_end_week_text_input"

        self.schema_alias = {"string": "string",
                             "list(struct(KEY: string, VALUE: int64))": "L[{S,I}]",
                             "list(struct(KEY: string, VALUE: string))": "L[{S,S}]"}
        self.landing_zone_submit_button = "landing_zone_submit_button"
