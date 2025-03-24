import json
import dash_auth
import dash_mantine_components as dmc
from dash import html

# pylint: disable=wildcard-import, unused-wildcard-import
from cornea_callbacks import *
from cornea_components import header
from cornea_configs import CorneaConfigs
from cornea_utils import CorneaUtils
from initialize_cache import app

cornea_configs = CorneaConfigs()
cornea_utils = CorneaUtils()


app.title = cornea_configs.app_title
server = app.server

auth = dash_auth.BasicAuth(
    app=app,
    username_password_list=json.loads(cornea_utils.access_secret_version(
        project_id=cornea_configs.project_id,
        secret_id=cornea_configs.cornea_credentials_key,
        version_id="latest"
    ))
)


app.layout = dmc.MantineProvider(
    id=cornea_configs.app_theme_id,
    theme={
        "colorScheme": "white",
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        html.Div([
            header,
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab("Dag Runs", value=cornea_configs.dag_runs_tab_id),
                            dmc.Tab("Landing Zone", value=cornea_configs.landing_zone_tab_id),
                            dmc.Tab("Archive Zone", value=cornea_configs.archive_zone_tab_id),
                            dmc.Tab("Available Data", value=cornea_configs.available_data_logs_tab_id),
                        ]
                    ),
                ],
                id=cornea_configs.tabs_list_id,
                value=cornea_configs.dag_runs_tab_id,
                variant="outline"
            ),
            html.Div(id=cornea_configs.tabs_content_id, style={"paddingTop": 10}),
        ])
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
