import dash

from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/landing-zone')

from components.cornea_components import navbar, datetimepicker, dropdown, sidebar, all_collapse

landing_zone = html.Div([
    navbar,
    dbc.Row([
        dbc.Col(md=2, children=sidebar),
        dbc.Col([
            dbc.Container([
                dbc.Row([dbc.Col(datetimepicker)]),
                dbc.Row([dbc.Col(dropdown)]),
                dbc.Row([dbc.Col(all_collapse)]),
            ], fluid=True),
        ])
    ])
])
