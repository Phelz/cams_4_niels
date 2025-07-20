import dash
import dash_bootstrap_components as dbc


zone_cams_ids = [37, 38, 39, 41, 45, 52, 54, 56, 57, 59, 60, 61, 67]

def camera_card(cam_id):
    return dbc.Card(
        [
            dbc.CardImg(src=f"/video_feed/{cam_id}", top=True, style={"height": "300px", "objectFit": "cover"}),
        ],
        style={"width": "22rem", "margin": "10px"},
    )


def create_layout(App: dash.Dash, server=None) -> dash.html.Div:
    # Group camera IDs into chunks of 3
    cam_chunks = [zone_cams_ids[i:i+3] for i in range(0, len(zone_cams_ids), 3)]

    return dash.html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(camera_card(cam_id), width=4)
                    for cam_id in chunk
                ],
                justify="start",
                className="g-2",
            )
            for chunk in cam_chunks
        ],
        style={"display": "block"},
    )