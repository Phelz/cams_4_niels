import dash
import dash_bootstrap_components as dbc
import time 
from dash import html, Output, Input
from dash_extensions import WebSocket

zone_cams_ids = [37, 38, 39, 41, 45, 52, 54, 56, 57, 59,  61, 67]
# zone_cams_ids = [ 59, 60, 61, 67]

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
    
    # Create a clientside callback for each camera to update the image source
    for cam_id in zone_cams_ids:
        App.clientside_callback(
            f"function(m){{return m? m.data : '';}}",
            Output(f"video-{cam_id}", "src"),
            Input(f"ws-{cam_id}", "message")
        )
    
    # Hardcode each row and column using the camera ids
    return dash.html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(camera_card(67), width=4),
                    dbc.Col(camera_card(61), width=4),
                    dbc.Col(camera_card(60), width=4),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(camera_card(59), width=4),
                    dbc.Col(camera_card(57), width=4),
                    dbc.Col(camera_card(56), width=4),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(camera_card(54), width=4),
                    dbc.Col(camera_card(52), width=4),
                    dbc.Col(camera_card(45), width=4),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(camera_card(41), width=4),
                    dbc.Col(camera_card(39), width=4),
                    dbc.Col(camera_card(38), width=4),
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(camera_card(37), width=4),
                ],
            ),
        ],
        # style={"display": "block"},
    )

# def create_layout(App: dash.Dash, server=None) -> dash.html.Div:
#     # Group camera IDs into chunks of 3
#     cam_chunks = [zone_cams_ids[::-1][i:i+3] for i in range(0, len(zone_cams_ids), 3)]
#     print('Zone')
#     print(cam_chunks)

#     row1 = dbc.Row(
#         [
#             dbc.Col(camera_card(cam_id), width=4)
#             for cam_id in cam_chunks[0]
#         ],
#         justify="start",
#         className="g-2",
#     )
#     row2 = dbc.Row(
#         [
#             dbc.Col(camera_card(cam_id), width=4)
#             for cam_id in cam_chunks[1]
#         ],
#         justify="start",
#         className="g-2",
#     )
#     row3 = dbc.Row(
#         [
#             dbc.Col(camera_card(cam_id), width=4)
#             for cam_id in cam_chunks[2]
#         ],
#         justify="start",
#         className="g-2",
#     )
#     return dash.html.Div(
#         [
#             row1,
#             row2,
#             row3
#         ],
#         style={"display": "block"},
#     )

    # return dash.html.Div(
    #     [
    #         dbc.Row(
    #             [
    #                 dbc.Col(camera_card(cam_id), width=4)
    #                 for cam_id in chunk
    #             ],
    #             justify="start",
    #             className="g-2",
    #         )
    #         for chunk in cam_chunks
    #     ],
    #     style={"display": "block"},
    # )