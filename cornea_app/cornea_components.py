from datetime import datetime
import dash_mantine_components as dmc

from cornea_configs import CorneaConfigs
from cornea_utils import CorneaUtils


cornea_configs = CorneaConfigs()
cornea_utils = CorneaUtils()


header = dmc.Header(
    height=130,
    withBorder=True,
    style={"padding": "16px", "display": "flex"},
    children=[
        dmc.Image(src="https://www.shutterstock.com/image-vector/blue-eye-iris-vector-format-600nw-2176690289.jpg",
                  height="50px", width=50
                  ),
        dmc.Text(
            "   Cornea",
            style={"fontSize": 30},
            align="left",
            weight=6000
        ),
        dmc.TextInput(
            id=cornea_configs.global_pwk_start_week_text_input,
            label="Global pwk_start_week",
            required=True,
            placeholder="YYYYWW",
            py=10,
            style={"width": 170, "margin-left": "100px"},
            value=datetime.now().strftime("%Y%W"),
        ),
        dmc.TextInput(
            id=cornea_configs.global_pwk_end_week_text_input,
            label="Global pwk_end_week",
            required=True,
            placeholder="YYYYWW",
            py=10,
            style={"width": 170, "margin-left": "30px"},
            value=datetime.now().strftime("%Y%W"),
        ),
        dmc.Switch(
            id="switch-theme",
            size="lg",
            radius="sm",
            label="Light Mode",
            offLabel="off",
            checked=True,
            ml="auto",
        ),
    ],
)
