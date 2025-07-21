import dash
from dash import  Output, Input
import dash_bootstrap_components as dbc

import components
from dash_extensions import WebSocket

from rich import print


def create_layout(App: dash.Dash) -> dash.html.Div:
    
    for cam_id in range(30, 70):
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