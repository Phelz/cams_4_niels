import dash_bootstrap_components as dbc

from dash import html
from dash_extensions import WebSocket

import config

def create_camera_card(cam_id: int) -> dbc.Card:
    ''' Create a camera card with a WebSocket and an image element. The socket URL is dynamically generated based on the camera ID. '''
    
    return dbc.Card(
        [
            WebSocket(
                url=f"ws://{config.SERVER_IP}:{config.QUART_SERVER_PORT}/video_feed/{cam_id}",
                id=f"ws-{cam_id}"),
            html.Img(
                       src=f"/video_feed/{cam_id}",
                       id=f"video-{cam_id}",
                       style={'width': '100%'})
        ],
        style={ "margin": "1px"},
    )