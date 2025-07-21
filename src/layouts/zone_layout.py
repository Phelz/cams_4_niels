import dash_bootstrap_components as dbc
import dash
import utils
import config


def create_layout(App: dash.Dash, server=None) -> dash.html.Div:
    
    zone_cams_ids = config.CAMS_LABELS['Zone']
        
    # Group camera IDs into chunks of 3
    cam_chunks = [zone_cams_ids[i:i+3] for i in range(0, len(zone_cams_ids), 3)]
    

    return dash.html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(utils.plotly_utils.create_camera_card(cam_id), width=4)
                    for cam_id in chunk
                ],
            )
            for chunk in cam_chunks
        ],
        # style={"display": "block"},
    )