import dash_bootstrap_components as dbc
import dash
from dash import html, Output, Input
import time
from dash_extensions import WebSocket

platform_cams_ids = [35, 40, 43, 51, 57, 60, 62, 63, 65, 66, 68]

def camera_card(cam_id):
    return dbc.Card(
        [
            # dbc.CardImg(src=f"/video_feed/{cam_id}", top=True, style={"height": "300px", "objectFit": "cover"}),
            WebSocket(
                url=f"ws://127.0.1:5000/video_feed/{cam_id}",
                id=f"ws-{cam_id}"),
            html.Img(
                       src=f"/video_feed/{cam_id}",
                       id=f"video-{cam_id}",
                    #    controls=False,
                       style={'width': '100%'})
        ],
        style={ "margin": "1px"},
    )



def create_layout(App: dash.Dash, server=None) -> dash.html.Div:
    
    
    # for cam_id in platform_cams_ids:
    #     App.clientside_callback(
    #         f"function(m){{return m? m.data : '';}}",
    #         Output(f"video-{cam_id}", "src"),
    #         Input(f"ws-{cam_id}", "message")
    #     )
        
    # Group camera IDs into chunks of 3
    cam_chunks = [platform_cams_ids[i:i+3] for i in range(0, len(platform_cams_ids), 3)]
    print('Platform')
    

    return dash.html.Div(
        [
            # dbc.Row(
            #     [
            #         dbc.Col(camera_card(cam_id), width=4)
            #         for cam_id in chunk
            #     ],
            # )
            # for chunk in cam_chunks
        ],
        # style={"display": "block"},
    )