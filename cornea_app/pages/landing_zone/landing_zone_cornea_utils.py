from datetime import datetime, timedelta
import pandas as pd
from plotly import express as px
import dash_mantine_components as dmc
from google.cloud import firestore
from dash import html

from initialize_cache import cache
from cornea_utils import CorneaUtils
from pages.landing_zone.landing_zone_cornea_configs import LandingZoneCorneaConfigs
from pages.landing_zone.landing_zone_components.row_count_card import row_count_card, row_count_insights_card
from pages.landing_zone.landing_zone_components.null_count_card import null_count_content
from pages.landing_zone.landing_zone_components.min_value_card import min_values_content
from pages.landing_zone.landing_zone_components.max_value_card import max_values_content
from pages.landing_zone.landing_zone_components.piechart_card import landing_zone_schema_piechart_card

cornea_utils = CorneaUtils()
landing_zone_cornea_configs = LandingZoneCorneaConfigs()
firestore_client = firestore.Client(
    project=landing_zone_cornea_configs.cornea_configs.project_id,
    database=landing_zone_cornea_configs.cornea_configs.firestore_database
)


class LandingZoneCorneaUtils:
    def __init__(self):
        pass

    @cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_features_list(self, table_id, dates=None):
        table_doc = firestore_client.document(f"landing_zone/{table_id}")
        features_list = []
        if dates is None:
            for feature in next(table_doc.collections()).get():
                features_list.append(feature.id)
        else:
            initial_date, final_date = cornea_utils.cornea_utils.get_initial_and_final_date(
                start_date=dates[0], end_date=dates[-1]
            )
            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            for date_str in date_range:
                collection = firestore_client.collection(f"landing_zone/{table_id}/{date_str}")
                for doc_ref in collection.get():
                    features_list.append(doc_ref.id)
                break
        features_list = [i for i in features_list if i not in ["CID", "HID"]]
        return features_list

    @cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_min_max_values_chart(self, landing_id, dates, features, is_light_mode, metric_type):
        features = self.get_features_list(table_id=landing_id) if features in [None, []] else features
        try:
            initial_date, final_date = cornea_utils.cornea_utils.get_initial_and_final_date(
                start_date=dates[0], end_date=dates[-1]
            )

            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            plot_data = []
            for date_str in date_range:
                collection = firestore_client.collection(f"landing_zone/{landing_id}/{date_str}")
                for doc_ref in collection.get():
                    if doc_ref.id not in ["CID", "HID"] and doc_ref.id in features:
                        doc_dict = doc_ref.to_dict()
                        temp_value = doc_dict.get(metric_type)
                        if temp_value is not None and temp_value.replace(",", "").isnumeric():
                            plot_data.append(
                                dict(
                                    pwk_week_timestamp=datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                    pwk_week=datetime.strftime(
                                        datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                        "%Y%W"
                                    ),
                                    values=doc_dict[metric_type],
                                    column_name=doc_ref.id
                                )
                            )

            plot_data = pd.DataFrame(data=plot_data)
            if len(plot_data) > 0:
                fig = px.bar(
                    plot_data, x="pwk_week", y="values", color='column_name',
                    title=f"{metric_type} for {landing_id} in date range {initial_date.date()} - {final_date.date()}",
                    template="plotly_dark" if not is_light_mode else "plotly"
                )
                temp_df = plot_data
                features_min_content = [
                    dmc.Text(f"{feature}:{temp_df.loc[temp_df['column_name'] == feature]['values'].min()}")
                    for feature in list(temp_df['column_name'].unique())
                ]

                features_max_content = [
                    dmc.Text(f"{feature}:{temp_df.loc[temp_df['column_name'] == feature]['values'].max()}")
                    for feature in list(temp_df['column_name'].unique())
                ]

                features_drift = [
                    dmc.Text(
                        f"""{feature}:{
                        float(temp_df.loc[
                                  temp_df.loc[temp_df["column_name"] == feature]["pwk_week_timestamp"].idxmax()
                              ]["values"])
                        - float(temp_df.loc[
                                    temp_df.loc[temp_df["column_name"] == feature]["pwk_week_timestamp"].idxmin()
                                ]["values"])
                        }"""
                    ) for feature in list(temp_df['column_name'].unique())
                ]
            else:
                fig = cornea_utils.no_figure_chart(
                    text_to_show=f"No data {landing_id} - date range of {initial_date.date()} - {final_date.date()}",
                    is_light_mode=is_light_mode
                )
                features_min_content, features_max_content, features_drift = \
                    [dmc.Text("No data to show")] * 3
        except Exception as e:
            fig = cornea_utils.no_figure_chart(
                text_to_show=f"You need to select landing_id and the date range. {e}",
                is_light_mode=is_light_mode
            )
            features_min_content, features_max_content, features_drift = \
                [dmc.Text("Select landing_id and daterange")] * 3
        return fig, features_min_content, features_max_content, features_drift, None

    @cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_null_count_chart(self, landing_id, dates, features, is_light_mode):
        features = self.get_features_list(table_id=landing_id) if features is None else features
        try:
            initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])

            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            null_count_plot_data = []
            for date_str in date_range:
                collection = firestore_client.collection(f"landing_zone/{landing_id}/{date_str}")
                for doc_ref in collection.get():
                    if doc_ref.id not in ["CID", "HID"] and doc_ref.id in features:
                        doc_dict = doc_ref.to_dict()
                        if doc_dict.get("null_values_count"):
                            null_count_plot_data.append(
                                dict(
                                    pwk_week_timestamp=datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                    pwk_week=datetime.strftime(
                                        datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                        "%Y%W"
                                    ),
                                    null_count=doc_dict["null_values_count"],
                                    column_name=doc_ref.id
                                )
                            )

            null_count_plot_data = pd.DataFrame(data=null_count_plot_data)

            if len(null_count_plot_data) > 0:
                fig = px.line(
                    null_count_plot_data, x="pwk_week", y="null_count", color='column_name',
                    title=f"Null count for {landing_id} in date range {initial_date.date()} - {final_date.date()}",
                    template="plotly_dark" if not is_light_mode else "plotly"
                )
                # fig.update_traces(textposition="bottom right")
                null_count_total_columns = len(null_count_plot_data["column_name"].unique())
                null_count_min_value = format(min(null_count_plot_data["null_count"]), ",")
                null_count_max_value = format(max(null_count_plot_data["null_count"]), ",")

                temp_df = null_count_plot_data
                null_count_features_min_content = [
                    dmc.Text(f"{feature}:{temp_df.loc[temp_df['column_name'] == feature]['null_count'].min()}")
                    for feature in list(temp_df['column_name'].unique())
                ]

                null_count_features_max_content = [
                    dmc.Text(f"{feature}:{temp_df.loc[temp_df['column_name'] == feature]['null_count'].max()}")
                    for feature in list(temp_df['column_name'].unique())
                ]

                features_drift = [
                    dmc.Text(
                        f"""{feature}:{
                        temp_df.loc[
                            temp_df.loc[temp_df["column_name"] == feature]["pwk_week_timestamp"].idxmax()
                        ]["null_count"]
                        - temp_df.loc[
                            temp_df.loc[temp_df["column_name"] == feature]["pwk_week_timestamp"].idxmin()
                        ]["null_count"]
                        }"""
                    ) for feature in list(temp_df['column_name'].unique())
                ]

            else:
                fig = cornea_utils.no_figure_chart(
                    text_to_show=f"No data {landing_id} - date range of {initial_date.date()} - {final_date.date()}",
                    is_light_mode=is_light_mode
                )
                null_count_total_columns, null_count_min_value, null_count_max_value = 0, 0, 0
                null_count_features_min_content, null_count_features_max_content, features_drift = \
                    [dmc.Text("No data to show")] * 3

        except Exception as e:
            fig = cornea_utils.no_figure_chart(
                text_to_show=f"You need to select landing_id and the date range. {e}",
                is_light_mode=is_light_mode
            )
            null_count_total_columns, null_count_min_value, null_count_max_value = 0, 0, 0
            null_count_features_min_content, null_count_features_max_content, features_drift = \
                [dmc.Text("Select landing_id and daterange")] * 3

        return fig, null_count_total_columns, null_count_min_value, null_count_max_value, \
            null_count_features_min_content, null_count_features_max_content, features_drift, None

    @cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
    def generate_pie_chart(self, landing_id, dates, is_light_mode):
        try:
            initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            schema_plot_data = []
            for date_str in date_range:
                collection = firestore_client.collection(f"landing_zone/{landing_id}/{date_str}")
                for doc_ref in collection.get():
                    if doc_ref.id not in ["CID", "HID"]:
                        doc_dict = doc_ref.to_dict()
                        schema = doc_dict.get("schema")
                        if schema is not None:
                            schema_plot_data.append(
                                dict(
                                    schema=landing_zone_cornea_configs.schema_alias[schema],
                                )
                            )

            schema_plot_data = pd.DataFrame(data=schema_plot_data)

            if len(schema_plot_data) > 0:
                fig = px.pie(schema_plot_data, names='schema', title='Landing zone schema')
            else:
                fig = cornea_utils.no_figure_chart(
                    text_to_show=f"No data {landing_id} - date range of {initial_date.date()} - {final_date.date()}",
                    is_light_mode=is_light_mode
                )
        except Exception as e:
            fig = cornea_utils.no_figure_chart(
                text_to_show=f"You need to select landing_id and the date range. {e}",
                is_light_mode=is_light_mode
            )
        return fig, None

    @cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_row_count_chart_and_insights(self, landing_id, dates, is_light_mode):
        try:
            initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            row_count_plot_data = []
            for date_str in date_range:
                collection = firestore_client.collection(f"landing_zone/{landing_id}/{date_str}")
                for doc_ref in collection.get():
                    doc_dict = doc_ref.to_dict()
                    row_count_plot_data.append(
                        dict(
                            pwk_week=datetime.strftime(
                                datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                "%Y%W"
                            ),
                            row_count=int(doc_dict["row_count"])
                        )
                    )
                    break

            row_count_plot_data = pd.DataFrame(data=row_count_plot_data)

            if len(row_count_plot_data) > 0:
                fig = px.line(
                    row_count_plot_data, x="pwk_week", y="row_count",
                    title=f"Row count for {landing_id} in date range {initial_date.date()} - {final_date.date()}",
                    template="plotly_dark" if not is_light_mode else "plotly")
                row_count_total_records, row_count_min_value, row_count_max_value = len(row_count_plot_data), \
                    format(min(row_count_plot_data["row_count"]), ","), \
                    format(max(row_count_plot_data["row_count"]), ",")

            else:
                fig = cornea_utils.no_figure_chart(
                    text_to_show=f"No data {landing_id} - date range of {initial_date.date()} - {final_date.date()}",
                    is_light_mode=is_light_mode
                )
                row_count_total_records, row_count_min_value, row_count_max_value = 0, 0, 0

        except Exception as e:
            fig = cornea_utils.no_figure_chart(
                text_to_show=f"You need to select landing_id and the date range - {e}",
                is_light_mode=is_light_mode
            )
            row_count_total_records, row_count_min_value, row_count_max_value = 0, 0, 0

        return fig, row_count_total_records, row_count_min_value, row_count_max_value, None

    @cache.memoize(timeout=landing_zone_cornea_configs.cornea_configs.cache_timeout)
    def render_landing_zone_content(self, active):
        if active == landing_zone_cornea_configs.row_count_card:
            content = html.Div(
                [
                    row_count_insights_card,
                    row_count_card,
                ],
                style={"padding": "32px", "display": "flex",
                       "justifyContent": "space-between"}
            )
        elif active == landing_zone_cornea_configs.null_count_card:
            content = html.Div(
                [
                    null_count_content
                ],
                style={"padding": "32px", "display": "flex",
                       "justifyContent": "space-between"}
            )
        elif active == landing_zone_cornea_configs.min_values_card:
            content = html.Div(
                [
                    min_values_content,
                ],
                style={"padding": "32px", "display": "flex",
                       "justifyContent": "space-between"}
            )
        elif active == landing_zone_cornea_configs.max_values_card:
            content = html.Div(
                [
                    max_values_content,

                ],
                style={"padding": "32px", "display": "flex",
                       "justifyContent": "space-between"}
            )
        elif active == landing_zone_cornea_configs.other_charts:
            content = html.Div(
                [
                    landing_zone_schema_piechart_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        else:
            content = [dmc.Text("Wrong Tab Selected")]
        return content
