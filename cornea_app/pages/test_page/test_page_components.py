import dash_mantine_components as dmc
from dash import dcc, Input, Output, callback


import plotly.express as px
import numpy as np
import pandas as pd

# df = pd.read_csv("percentile_bins.csv")
# create the bins
# counts, bins = np.histogram(df.total_bill, bins=range(0, 60, 5))
# bins = 0.5 * (bins[:-1] + bins[1:])

percentile_bins = np.array([0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 6.71751440e-01, 1.72627735e+00, 2.47922564e+00,
       3.19140863e+00, 3.93151379e+00, 4.69165373e+00, 5.51946878e+00,
       6.44527817e+00, 7.50947380e+00, 8.80000019e+00, 1.03572588e+01,
       1.24733639e+01, 1.53666668e+01, 2.00850315e+01, 3.05470123e+01,
       6.79317480e+03])

fig = px.bar(x=list(range(0, 105, 5)), y=percentile_bins, labels={'x': 'percentile_bins', 'y': 'value'})

histogram_plot_chart = dcc.Graph(id="histogram_plot_chart", style={"padding": "20px"}, figure=fig)

histogram_plot_card = dmc.Card(
    children=[
        dmc.Text("Avg Values Chart"),
        dmc.CardSection(histogram_plot_chart),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"height": 500, "width": 1300, "margin": "20px"},
)


# @callback(
#     Output("histogram_plot_chart", "figure")
# )
# def get_average_values_chart(values, dates, features=None, is_light_mode=None):
#     import plotly.express as px
#     import numpy as np
#
#     df = px.data.tips()
#     # create the bins
#     counts, bins = np.histogram(df.total_bill, bins=range(0, 60, 5))
#     bins = 0.5 * (bins[:-1] + bins[1:])
#
#     fig = px.bar(x=bins, y=counts, labels={'x': 'total_bill', 'y': 'count'})
#     # fig.show()
#     return fig