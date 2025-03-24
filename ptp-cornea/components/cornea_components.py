from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import plotly.express as px
import pandas as pd
import json

from google.cloud import storage
storage_client = storage.Client()


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
    ],
    brand="PTP-Cornea",
    brand_href="/",
    sticky="top",
    color="light",
    brand_style={
        'font-size': '2em'
    },
)

sidebar = html.Div(
    [
        html.H2("Zone", className="display-4", style={'font-size': '1.5em'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Landing Zone", href="/landing-zone", id="landing-zone-link", style={'color': 'darkgray'}),
                dbc.NavLink("TransformHub", href="/transformhub", id="transformhub-link", style={'color': 'darkgray'}),
                dbc.NavLink("Archive Zone", href="/archive-zone", id="archive-zone-link", style={'color': 'darkgray'}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        'padding': '20px',
        'backgroundColor': 'lightgray',
        'height': '100vh'
    }
)

datetimepicker = html.Div([
    dcc.DatePickerRange(
        id='datetimepicker_id',
        start_date=datetime.now().date() - timedelta(days=7),
        end_date=datetime.now().date()
    ),
    html.Div(id='datetimepicker_output')
])

dropdown = html.Div([
    dcc.Dropdown(
        ['grocery_behavior_wk', 'ent_sales_wk', 'offer_attributes_mt',
         'pco_data_mt', 'promo_sdm_sales', 'sdm_behavior_wk'],
        # 'grocery_behavior_wk',
        id='dropdown_id'),
    html.Div(id='dropdown_output')
])

submitbutton = html.Div([
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic')
])


def nofigurechart(text_to_show):
    fig = go.Figure()

    return fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
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


def get_initial_and_final_date(start_date, end_date):
    start_date = pd.to_datetime(date.fromisoformat(start_date))
    end_date = pd.to_datetime(date.fromisoformat(end_date))

    initial_date = start_date
    final_date = end_date
    if start_date > end_date:
        initial_date = end_date
        final_date = start_date
    return initial_date, final_date


def get_metadata_file(landing_id_value):
    bucket = storage_client.get_bucket('exp-ptp-logging-monitoring')
    blob = bucket.blob(f"metadata_jsons/{landing_id_value}.json")
    data = json.loads(blob.download_as_string(client=None))

    # data = json.load(open(f"metadata_jsons/{landing_id_value}.json"))
    return data


null_count_chart = dcc.Graph(id="null_count_chart")


@callback(
    Output("null_count_chart", "figure"),
    Input("dropdown_id", "value"),
    Input('datetimepicker_id', 'start_date'),
    Input('datetimepicker_id', 'end_date')
)
def get_null_count_chart(value, start_date, end_date):
    try:
        initial_date, final_date = get_initial_and_final_date(start_date, end_date)

        date_range = [f"{x.year}/{x.month}/{x.day}" for x in pd.date_range(start=initial_date, end=final_date)]
        metadata_dict = get_metadata_file(landing_id_value=value)

        plot_data = pd.DataFrame(data=[], columns=["date", "column_name", "null_count"])
        for date_str in date_range:
            date_metadata = metadata_dict.get(date_str, None)
            if date_metadata:
                for key, null_count_value in date_metadata['null_values_count'].items():
                    plot_data = pd.concat(
                        [plot_data, pd.DataFrame([{"date": date_str, "column_name": key, "null_count": null_count_value}])]
                    )

        if len(plot_data) > 0:
            fig = px.line(plot_data, x="date", y="null_count", color='column_name', title=f"Null count for {value} in date range {initial_date.date()} - {final_date.date()}")
        else:
            fig = nofigurechart(
                text_to_show=f"No data for {value} - date range of {initial_date.date()} - {final_date.date()}"
            )
    except Exception as E:
        fig = nofigurechart(
            text_to_show=f"You need to select landing_id and the date range. {E}"
        )
    return fig


row_count_chart = dcc.Graph(id="row_count_chart")


@callback(
    Output("row_count_chart", "figure"),
    Input("dropdown_id", "value"),
    Input('datetimepicker_id', 'start_date'),
    Input('datetimepicker_id', 'end_date')
)
def get_row_count_chart(value, start_date, end_date):
    try:
        initial_date, final_date = get_initial_and_final_date(start_date, end_date)

        date_range = [f"{x.year}/{x.month}/{x.day}" for x in pd.date_range(start=initial_date, end=final_date)]
        metadata_dict = get_metadata_file(landing_id_value=value)

        row_count_plot_data = pd.DataFrame(data=[], columns=["date", "row_count"])
        for date_str in date_range:
            date_metadata = metadata_dict.get(date_str, None)
            if date_metadata:
                row_count_value = date_metadata.get("row_count", None)
                row_count_plot_data = pd.concat(
                        [row_count_plot_data, pd.DataFrame([{"date": date_str, "row_count": row_count_value}])]
                    )

        if len(row_count_plot_data) > 0:
            fig = px.line(row_count_plot_data, x="date", y="row_count", title=f"Row count for {value} in date range {initial_date.date()} - {final_date.date()}")
        else:
            fig = nofigurechart(
                text_to_show=f"No data for {value} - date range of {initial_date.date()} - {final_date.date()}"
            )
    except Exception as E:
        fig = nofigurechart(
            text_to_show=f"You need to select landing_id and the date range - {E}"
        )
    return fig


min_values_chart = dcc.Graph(id="min_values_chart")


@callback(
    Output("min_values_chart", "figure"),
    Input("dropdown_id", "value"),
    Input('datetimepicker_id', 'start_date'),
    Input('datetimepicker_id', 'end_date')
)
def get_min_values_chart(value, start_date, end_date):
    try:
        initial_date, final_date = get_initial_and_final_date(start_date, end_date)

        date_range = [f"{x.year}/{x.month}/{x.day}" for x in pd.date_range(start=initial_date, end=final_date)]
        metadata_dict = get_metadata_file(landing_id_value=value)

        plot_data = pd.DataFrame(data=[], columns=["date", "column_name", "min_values"])
        for date_str in date_range:
            date_metadata = metadata_dict.get(date_str, None)
            if date_metadata:
                for key, min_value in date_metadata['min_values_count'].items():
                    plot_data = pd.concat(
                        [plot_data,
                         pd.DataFrame([{"date": date_str, "column_name": key, "min_values": min_value}])]
                    )

        if len(plot_data) > 0:
            fig = px.bar(plot_data, x="date", y="min_values", color='column_name',
                          title=f"Min values for {value} in date range {initial_date.date()} - {final_date.date()}")
        else:
            fig = nofigurechart(
                text_to_show=f"No data for {value} - date range of {initial_date.date()} - {final_date.date()}"
            )
    except Exception as E:
        fig = nofigurechart(
            text_to_show=f"You need to select landing_id and the date range. {E}"
        )
    return fig


max_values_chart = dcc.Graph(id="max_values_chart")


@callback(
    Output("max_values_chart", "figure"),
    Input("dropdown_id", "value"),
    Input('datetimepicker_id', 'start_date'),
    Input('datetimepicker_id', 'end_date')
)
def get_min_values_chart(value, start_date, end_date):
    try:
        initial_date, final_date = get_initial_and_final_date(start_date, end_date)

        date_range = [f"{x.year}/{x.month}/{x.day}" for x in pd.date_range(start=initial_date, end=final_date)]
        metadata_dict = get_metadata_file(landing_id_value=value)

        plot_data = pd.DataFrame(data=[], columns=["date", "column_name", "max_values"])
        for date_str in date_range:
            date_metadata = metadata_dict.get(date_str, None)
            if date_metadata:
                for key, max_value in date_metadata['max_values_count'].items():
                    plot_data = pd.concat(
                        [plot_data,
                         pd.DataFrame([{"date": date_str, "column_name": key, "max_values": max_value}])]
                    )

        if len(plot_data) > 0:
            fig = px.bar(plot_data, x="date", y="max_values", color='column_name',
                          title=f"Max values for {value} in date range {initial_date.date()} - {final_date.date()}")
        else:
            fig = nofigurechart(
                text_to_show=f"No data for {value} - date range of {initial_date.date()} - {final_date.date()}"
            )
    except Exception as E:
        fig = nofigurechart(
            text_to_show=f"You need to select landing_id and the date range. {E}"
        )
    return fig


all_collapse = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(
                    "Null Count",
                    id="null_count_collapse_button",
                    className="mb-3 btn btn-dark",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Row([
                    dbc.Col(
                        dbc.Collapse(
                            null_count_chart,
                            id="null_count_collapse",
                            is_open=False
                        )
                    )
                ])
            ], className="d-grid")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(
                    "Row Count",
                    id="row_count_collapse_button",
                    className="mb-3 btn btn-dark",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Row([
                    dbc.Col(
                        dbc.Collapse(
                            row_count_chart,
                            id="row_count_collapse",
                            is_open=False
                        )
                    )
                ])
            ], className="d-grid")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(
                    "Min Values",
                    id="min_values_collapse_button",
                    className="mb-3 btn btn-dark",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Row([
                    dbc.Col(
                        dbc.Collapse(
                            min_values_chart,
                            id="min_values_collapse",
                            is_open=False
                        )
                    )
                ])
            ], className="d-grid")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button(
                    "Max Values",
                    id="max_values_collapse_button",
                    className="mb-3 btn btn-dark",
                    color="primary",
                    n_clicks=0,
                ),
                dbc.Row([
                    dbc.Col(
                        dbc.Collapse(
                            max_values_chart,
                            id="max_values_collapse",
                            is_open=False
                        )
                    )
                ])
            ], className="d-grid")
        ])
    ])
])


@callback(
    Output("row_count_collapse", "is_open"),
    [Input("row_count_collapse_button", "n_clicks")],
    [State("row_count_collapse", "is_open")],
)
def toggle_collapse_row_count(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("null_count_collapse", "is_open"),
    [Input("null_count_collapse_button", "n_clicks")],
    [State("null_count_collapse", "is_open")],
)
def toggle_collapse_null_values(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("min_values_collapse", "is_open"),
    [Input("min_values_collapse_button", "n_clicks")],
    [State("min_values_collapse", "is_open")],
)
def toggle_collapse_min_values(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("max_values_collapse", "is_open"),
    [Input("max_values_collapse_button", "n_clicks")],
    [State("max_values_collapse", "is_open")],
)
def toggle_collapse_max_values(n, is_open):
    if n:
        return not is_open
    return is_open
