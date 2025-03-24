import re
from datetime import date, datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from google.cloud import secretmanager

from cornea_configs import CorneaConfigs

cornea_configs = CorneaConfigs()


class CorneaUtils:
    def __init__(self):
        pass

    def no_figure_chart(self, text_to_show, is_light_mode):
        fig = go.Figure()

        return fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            template="plotly_dark" if not is_light_mode else "plotly",
            annotations=[
                {
                    "text": text_to_show,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 10
                    }
                }
            ]
        )

    def get_initial_and_final_date(self, start_date, end_date):
        start_date = pd.to_datetime(date.fromisoformat(start_date))
        end_date = pd.to_datetime(date.fromisoformat(end_date))

        initial_date = start_date
        final_date = end_date
        if start_date > end_date:
            initial_date = end_date
            final_date = start_date
        return initial_date, final_date

    def get_loading_spinner(self, spinner_component_id):
        return dcc.Loading(
            type="circle",
            children=html.Div(id=spinner_component_id),
            style={"align": "center"}
        )

    def week_pwk_format_error_text(self, text_start, text_end):
        regex_search = r"^[0-9]{6}"
        start_error_return = "Format is YYYYWW"
        end_error_return = "Format is YYYYWW"
        if text_start:
            if re.findall(regex_search, text_start) == [text_start] and len(text_start) == 6 and text_start.isdigit():
                start_error_return = None

        if text_end:
            if re.findall(regex_search, text_end) == [text_end] and len(text_end) == 6 and text_end.isdigit():
                end_error_return = None
        return start_error_return, end_error_return

    def date_picker_from_pwk(self, start_pwk, end_pwk):
        try:
            pwk_start_monday = datetime.strptime(f"{start_pwk} 1", "%Y%W %w")
            range_start_date = (pwk_start_monday - timedelta(days=4)).date()

            pwk_end_monday = datetime.strptime(f"{end_pwk} 1", "%Y%W %w")
            range_end_date = (pwk_end_monday + timedelta(days=2)).date()

            return [range_start_date, range_end_date]

        except ValueError:
            return [datetime.now().date() - timedelta(days=7), datetime.now().date()]

    def date_picker_error_text(self, dates):
        initial_date, final_date = self.get_initial_and_final_date(start_date=dates[0], end_date=dates[-1])
        initial_date = initial_date + timedelta(weeks=1)
        return f"Selected PWK range {initial_date.strftime('%Y%W')}-{final_date.strftime('%Y%W')}"

    def access_secret_version(self, project_id, secret_id, version_id):
        client = secretmanager.SecretManagerServiceClient()
        name = client.secret_version_path(project_id, secret_id, version_id)
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return str(payload)
