import dash
import dash_bootstrap_components as dbc

def camera_card(cam_id):
    return dbc.Card(
        [
            dbc.CardImg(src=f"/video_feed/{cam_id}", top=True, style={"height": "300px", "objectFit": "cover"}),
        ],
        style={"width": "22rem", "margin": "10px"},
    )


def create_layout(App: dash.Dash, server=None) -> dash.html.Div:
    return dash.html.Div(
        [
        ]
    )