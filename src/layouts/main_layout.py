import dash
from dash import  Output, Input
import dash_bootstrap_components as dbc

import components
from dash_extensions import WebSocket

from rich import print

CAMS_LABELS = {
    'Zone': [37, 38, 39, 41, 45, 52, 54, 56, 57, 59, 60, 61, 67],
    'Platform': [35, 40, 43, 51, 57, 60, 62, 63, 65, 66, 68],
    'Equipment' : [42, 44, 53, 69],
    'Helium': [39, 40, 61, 67 ],
    'Rooms' : [34, 36, 47, 48, 64, 69,]
}


def create_layout(App: dash.Dash) -> dash.html.Div:
    
    # ! Hardcoded. Need to know if there will be other cameras.
    for cam_id in range(30, 70):
    # for key, cam_ids in CAMS_LABELS.items():
    #     print(f"Creating layout for {key} with cameras: {cam_ids}")
    #     for cam_id in cam_ids:
            App.clientside_callback(
                f"function(m){{return m? m.data : '';}}",
                Output(f"video-{cam_id}", "src"),
                Input(f"ws-{cam_id}", "message")
            )
    
    
    layout = dash.html.Div(
        [
            dash.dcc.Location(id="url", refresh=True),
            components.nav_bar.render(App),
            dash.html.Div(id="page-content", children=[]),
            dash.page_container,
        ]
    )


    return layout