import dash
from dash import  Output, Input
import dash_bootstrap_components as dbc

import components
from dash_extensions import WebSocket

from rich import print

import config



def create_layout(App: dash.Dash) -> dash.html.Div:
    

    print(config.CAMS_LABELS)
    
    # ! Hardcoded. Need to know if there will be other cameras.
    # for cam_id in config.ALL_CAMS_IDS:
    for cam_id in range(min(config.ALL_CAMS_IDS),
                        max(config.ALL_CAMS_IDS) + 1
                        ):

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