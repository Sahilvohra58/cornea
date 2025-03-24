from dash import html
import dash
import dash_auth
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "PTP Cornea"
server = app.server

auth = dash_auth.BasicAuth(app, {"admin": "admin"})
from pages.landing_zone_page import landing_zone

app.layout = html.Div([
    landing_zone
    ])

if __name__ == '__main__':
    app.run(debug=True)
