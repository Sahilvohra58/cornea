from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from plotly import express as px
import plotly.graph_objects as go
from google.cloud import firestore
import gcsfs
import dash_mantine_components as dmc
from dash import html

from initialize_cache import cache
from pages.archive_zone.archive_zone_cornea_configs import ArchiveZoneCorneaConfigs
from pages.archive_zone.archive_zone_components.general_stats_cards.average_values_card import average_values_card, \
    average_values_drift_card
from pages.archive_zone.archive_zone_components.general_stats_cards.minimum_values_card import minimum_values_card, \
    minimum_values_drift_card
from pages.archive_zone.archive_zone_components.general_stats_cards.maximum_values_card import maximum_values_card, \
    maximum_values_drift_card
from pages.archive_zone.archive_zone_components.general_stats_cards.standard_deviation_values_card import \
    standard_deviation_values_card, standard_deviation_values_drift_card
from pages.archive_zone.archive_zone_components.general_stats_cards.skew_values_card import skew_values_card, \
    skew_values_drift_card
from pages.archive_zone.archive_zone_components.general_stats_cards.null_values_card import null_values_card, \
    null_values_drift_card
from pages.archive_zone.archive_zone_components.general_stats_cards.zero_values_card import zero_values_card, \
    zero_values_drift_card
from cornea_utils import CorneaUtils

cornea_utils = CorneaUtils()
archive_zone_cornea_configs = ArchiveZoneCorneaConfigs()
firestore_client = firestore.Client(
    project=archive_zone_cornea_configs.cornea_configs.project_id,
    database=archive_zone_cornea_configs.cornea_configs.firestore_database
)


class ArchiveZoneCorneaUtils:
    def __init__(self):
        pass

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_features_list(self, table_id, dates=None):
        table_doc = firestore_client.document(f"archive_zone/{table_id}")
        features_list = []
        if dates is None:
            for feature in next(table_doc.collections()).get():
                features_list.append(feature.id)
        else:
            initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            for date_str in date_range:
                collection = firestore_client.collection(f"archive_zone/{table_id}/{date_str}")
                for doc_ref in collection.get():
                    features_list.append(doc_ref.id)
                break
        return features_list

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_plot_dataframe(self, metric_type, table_id, dates, features):
        features = [] if features in [None, []] else features
        initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
        date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
        plot_data = []
        for date_str in date_range:
            collection = firestore_client.collection(f"archive_zone/{table_id}/{date_str}")
            for doc_ref in collection.get():
                doc_dict = doc_ref.to_dict()
                if not features:
                    metric_value = doc_dict.get(metric_type)
                    plot_data.append(
                        {
                            "pwk_week": datetime.strftime(
                                datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                "%Y%W"),
                            "feature_key": doc_ref.id,
                            metric_type: round(metric_value, 3) if metric_value is not None else metric_value
                        }
                    )
                else:
                    if doc_ref.id in features:
                        metric_value = doc_dict.get(metric_type)
                        plot_data.append(
                            {
                                "pwk_week": datetime.strftime(
                                    datetime.strptime(date_str, "%Y-%m-%d") + timedelta(weeks=1),
                                    "%Y%W"),
                                "feature_key": doc_ref.id,
                                metric_type: round(metric_value, 3) if metric_value is not None else metric_value
                            }
                        )

        plot_data = pd.DataFrame(data=plot_data)
        return plot_data

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_chart(
            self,
            metric_type,
            table_id,
            dates,
            features,
            chart_type,
            chart_label_switch=None,
            is_light_mode=None
    ):
        features = [] if features in [None, []] else features
        try:  # pylint: disable=too-many-nested-blocks
            initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
            plot_data = self.get_plot_dataframe(
                metric_type=metric_type,
                table_id=table_id,
                dates=dates,
                features=features
            )
            fig = None
            if len(plot_data) > 0:
                if chart_type == "Line chart":
                    fig = px.line(
                        data_frame=plot_data[["pwk_week", "feature_key", metric_type]],
                        x="pwk_week", y=metric_type, color="feature_key",
                        title=f"{metric_type} for {table_id} in date range {initial_date.date()} - {final_date.date()}",
                        text=metric_type,
                        template="plotly_dark" if not is_light_mode else "plotly"
                    )
                    fig.update_traces(textposition="bottom right")
                elif chart_type == "Bar chart":
                    fig = px.bar(
                        data_frame=plot_data, x="pwk_week", y=metric_type, color="feature_key",
                        title=f"{metric_type} for {table_id} in date range {initial_date.date()} - {final_date.date()}",
                        text=metric_type,
                        template="plotly_dark" if not is_light_mode else "plotly"
                    )
                if not chart_label_switch:
                    fig.update_traces(text=None)
                    fig.update_layout(showlegend=False)

            else:
                text_to_show = f"No data for {table_id} - date range of {initial_date.date()} - {final_date.date()}"

                fig = cornea_utils.no_figure_chart(
                    text_to_show=text_to_show,
                    is_light_mode=is_light_mode
                )

        except Exception as e:
            text_to_show = f"You need to select archive zone table ID and the date range - {e}"
            fig = cornea_utils.no_figure_chart(
                text_to_show=text_to_show,
                is_light_mode=is_light_mode
            )

        return fig

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_drifts_insights(self, metric_type, table_id, dates, features):
        features = [] if features in [None, []] else features
        plot_data = self.get_plot_dataframe(
            metric_type=metric_type,
            table_id=table_id,
            dates=dates,
            features=features
        )
        drift_values = {}
        plot_data = plot_data.dropna()
        if len(plot_data) > 0:
            plot_data["pwk_week"] = pd.to_numeric(plot_data["pwk_week"])
            min_pwk, max_pwk = plot_data["pwk_week"].min(), plot_data["pwk_week"].max()
            all_features = plot_data["feature_key"].unique()
            for feature_key in all_features:
                start_value = plot_data.loc[
                    (plot_data['pwk_week'] == min_pwk) & (plot_data['feature_key'] == feature_key)
                    ][metric_type].values[0]
                end_value = plot_data.loc[
                    (plot_data['pwk_week'] == max_pwk) & (plot_data['feature_key'] == feature_key)
                    ][metric_type].values[0]

                if not start_value:
                    percentage_drift = np.nan
                elif start_value == end_value:
                    percentage_drift = 0
                else:
                    percentage_drift = ((end_value - start_value) / start_value) * 100
                drift_values[feature_key] = str(round(percentage_drift, 2))
        return drift_values

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_drifts_content(self, table_id, dates, features, metric_type):
        try:
            drift_insights = self.get_drifts_insights(
                metric_type=metric_type, table_id=table_id, dates=dates, features=features
            )
            if drift_insights:
                display_content = [
                    dmc.Text(f"{feature_key}:{drift_percentage}") for feature_key, drift_percentage in
                    drift_insights.items()
                ]
            else:
                display_content = [dmc.Text("Nothing to show")]

        except Exception as e:
            display_content = [dmc.Text(f"Something went wrong - {e}")]
        return display_content

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_range_plot_content(self, table_id, dates, features, is_light_mode):
        features = [] if features is None else features
        line_colors = [(0, 100, 80, 0.2), (0, 176, 246, 0.2), (231, 107, 243, 0.2)]
        colors = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
        line_size = [2, 2, 4, 2]
        mode_size = [8, 8, 12, 8]
        colors_dict = dict(zip(features, line_colors))

        try:  # pylint: disable=too-many-nested-blocks
            initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])

            date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
            plot_data = []

            for date_str in date_range:
                collection = firestore_client.collection(f"archive_zone/{table_id}/{date_str}")
                for doc_ref in collection.get():
                    if doc_ref.id in features:
                        doc_dict = doc_ref.to_dict()
                        min_value = doc_dict.get("min_value")
                        max_value = doc_dict.get("max_value")
                        avg_value = doc_dict.get("avg_value")
                        std_value = doc_dict.get("std_value")

                        plot_data.append(
                            {
                                "pwk_week": datetime.strftime(datetime.strptime(date_str, "%Y-%m-%d"), "%Y%W"),
                                "feature_key": doc_ref.id,
                                "min_value": round(min_value, 3) if min_value is not None else min_value,
                                "max_value": round(max_value, 3) if max_value is not None else max_value,
                                "avg_value": round(avg_value, 3) if avg_value is not None else avg_value,
                                "std_value": round(std_value, 3) if std_value is not None else std_value,
                            }
                        )
            plot_data = pd.DataFrame(data=plot_data)

            if len(plot_data) > 0:
                fig = go.Figure()
                annotations = []
                for feature in features:

                    plot_data_dict = {
                        "pwk_week": list(plot_data["pwk_week"]), "min_value": list(plot_data["min_value"]),
                        "max_value": list(plot_data["max_value"]), "avg_value": list(plot_data["avg_value"]),
                        "std_value": list(plot_data["std_value"])}

                    all_metrics = ["min_value", "max_value", "avg_value", "std_value"]
                    for idx, plot_metric in enumerate(all_metrics):
                        fig.add_trace(go.Scatter(
                            y=plot_data_dict[plot_metric],
                            x=plot_data_dict["pwk_week"],
                            mode='lines',
                            name=f"{plot_metric}",
                            line=dict(color=colors[idx], width=line_size[idx]),
                            connectgaps=True,
                        ))

                        fig.add_trace(go.Scatter(
                            y=[plot_data_dict[plot_metric][0], plot_data_dict[plot_metric][-1]],
                            x=[plot_data_dict["pwk_week"][0], plot_data_dict["pwk_week"][-1]],
                            mode='markers',
                            marker=dict(color=colors[idx], size=mode_size[idx])
                        ))

                        # labeling the left_side of the plot
                        annotations.append(dict(
                            xref='paper', x=0.05, y=plot_data_dict[plot_metric][0],
                            xanchor='right', yanchor='middle',
                            text=f"{plot_metric}" + ' {}'.format(plot_data_dict[plot_metric][0]),
                            font=dict(family='Arial',
                                      size=16),
                            showarrow=False)
                        )

                        # labeling the right_side of the plot
                        annotations.append(dict(
                            xref='paper', x=0.95, y=plot_data_dict[plot_metric][-1],
                            xanchor='left', yanchor='middle',
                            text=' {}'.format(plot_data_dict[plot_metric][0]),
                            font=dict(family='Arial',
                                      size=16),
                            showarrow=False))

                    fig.update_layout(
                        xaxis=dict(
                            showline=True,
                            showgrid=False,
                            showticklabels=True,
                            linecolor='rgb(204, 204, 204)',
                            linewidth=2,
                            ticks='outside',
                            tickfont=dict(
                                family='Arial',
                                size=12,
                                color='rgb(82, 82, 82)',
                            ),
                        ),
                        yaxis=dict(
                            showgrid=False,
                            zeroline=False,
                            showline=False,
                            showticklabels=False,
                        ),
                        autosize=False,
                        margin=dict(
                            autoexpand=False,
                            l=100,
                            r=20,
                            t=110,
                        ),
                        showlegend=False,
                        plot_bgcolor='white'
                    )

                fig.update_layout(annotations=annotations)
                fig.update_layout(template="plotly_dark" if not is_light_mode else "plotly")

            else:
                text_to_show = f"No data for {table_id} - date range of {initial_date.date()} - {final_date.date()}"

                fig = cornea_utils.no_figure_chart(
                    text_to_show=text_to_show,
                    is_light_mode=is_light_mode
                )
        except Exception as e:
            text_to_show = f"You need to select archive zone table ID and the date range - {e}"
            fig = cornea_utils.no_figure_chart(
                text_to_show=text_to_show,
                is_light_mode=is_light_mode
            )
        return fig

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def get_percentile_box_plot_content(self, pwk_week, table_id, features, chart_type, is_light_mode):

        features = [] if features is None else features
        try:
            pwk_start_date = (datetime.strptime(f"{pwk_week} 1", "%Y%W %w") - timedelta(days=4)).strftime("%Y-%m-%d")
            collection = firestore_client.collection(f"archive_zone/{table_id}/{pwk_start_date}")
            percentile_bins = {}
            collection_metrics = "histogram_bins" if chart_type == "Histogram" else "percentile_bins"
            for doc_ref in collection.get():
                if doc_ref.id in features:
                    doc_dict = doc_ref.to_dict()
                    bin_values = doc_dict.get(collection_metrics)
                    if bin_values:
                        percentile_bins[doc_ref.id] = doc_dict[collection_metrics]

            fig = go.Figure()

            if percentile_bins:
                for feature_name, plot_data in percentile_bins.items():
                    if chart_type == "Box Plot":
                        fig.add_trace(go.Box(y=plot_data, name=feature_name, showlegend=False))
                    elif chart_type == "Percentile Bar Chart":
                        fig.add_trace(go.Bar(x=list(range(0, 105, 5)), y=plot_data, name=feature_name))
                    elif chart_type == "Histogram":
                        fig.add_trace(go.Bar(x=plot_data["x_axis"], y=plot_data["y_axis"], name=feature_name))

                if chart_type in ["Percentile Bar Chart", "Histogram"]:
                    fig.update_layout(barmode='group')
                fig.update_layout(template="plotly_dark" if not is_light_mode else "plotly")
            else:
                text_to_show = f"No data for {table_id} - for PWK {pwk_week} and feature {features}"

                fig = cornea_utils.no_figure_chart(
                    text_to_show=text_to_show,
                    is_light_mode=is_light_mode
                )

            return fig

        except Exception as e:
            text_to_show = f"You need to select archive zone table ID and PWK week - {e}"
            fig = cornea_utils.no_figure_chart(
                text_to_show=text_to_show,
                is_light_mode=is_light_mode
            )

        return fig

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def pwk_records_card_content(self, dates, table_id):
        initial_date, final_date = cornea_utils.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
        date_range = [x.strftime('%Y-%m-%d') for x in pd.date_range(start=initial_date, end=final_date)]
        pwk_record_count = 0
        for date_str in date_range:
            date_doc = firestore_client.collection(f"archive_zone/{table_id}/{date_str}")
            if len(list(date_doc.list_documents())) > 0:
                pwk_record_count += 1
        return pwk_record_count

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def total_selected_features_count(self, selected_features, table_id, dates):
        if selected_features is None:
            features_count = len(self.get_features_list(table_id=table_id, dates=dates))
        else:
            features_count = len(selected_features)
        return features_count

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def feature_type_cards_content(self, table_id, features):
        features = [] if features is None else features

        fs = gcsfs.GCSFileSystem()
        with fs.open(f'exp-ptp-logging-monitoring/temp_folder/unique values/{table_id}.csv') as f:
            df = pd.read_csv(f)

        # path = f"gs://exp-ptp-logging-monitoring/temp_folder/unique values/{table_id}.csv"
        # df = pd.read_csv(path)

        if features:
            df = df.loc[df['feature_key'].isin(features)]

        data_dict = {}
        if len(df) > 0:
            df["feature_type"] = df["unique_values"].apply(lambda x: "categorical" if x <= 20 else "continuous")
            data_dict = df["feature_type"].value_counts().to_dict()
        else:
            data_dict["categorical"], data_dict["continuous"] = 0, 0

        return data_dict["categorical"], data_dict["continuous"]

    @cache.memoize(timeout=archive_zone_cornea_configs.cornea_configs.cache_timeout)
    def render_archive_zone_content(self, active):
        if active == archive_zone_cornea_configs.average_values_card:
            content = html.Div(
                [
                    average_values_drift_card,
                    average_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        elif active == archive_zone_cornea_configs.minimum_values_card:
            content = html.Div(
                [
                    minimum_values_drift_card,
                    minimum_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        elif active == archive_zone_cornea_configs.maximum_values_card:
            content = html.Div(
                [
                    maximum_values_drift_card,
                    maximum_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        elif active == archive_zone_cornea_configs.standard_deviation_values_card:
            content = html.Div(
                [
                    standard_deviation_values_drift_card,
                    standard_deviation_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        elif active == archive_zone_cornea_configs.skew_values_card:
            content = html.Div(
                [
                    skew_values_drift_card,
                    skew_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        elif active == archive_zone_cornea_configs.null_values_card:
            content = html.Div(
                [
                    null_values_drift_card,
                    null_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        elif active == archive_zone_cornea_configs.zero_values_card:
            content = html.Div(
                [
                    zero_values_drift_card,
                    zero_values_card
                ],
                style={"padding": "32px", "display": "flex"}
            )
        else:
            content = [dmc.Text("Wrong Tab Selected")]
        return content
