import dash
from dash import dcc, html
import flask
from flask import Flask, Response
import dash_bootstrap_components as dbc
from quart import Quart, websocket
import cv2
from rich import print
# from datetime import datetime, timedelta
from dash_bootstrap_components.themes import LUX as THEME

import threading
# from src import definitions

# Configure the app
app = dash.Dash(
    __name__,
    server=Quart(__name__),
    # server=flask.Flask(__name__),
    title="Cams 4 Niels",
    external_stylesheets=[THEME],
    use_pages=True,
    meta_tags=[
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"},
    ],
)

server = app.server


CAMS_LABELS = {
    'Zone': [37, 38, 39, 41, 45, 52, 54, 56, 57, 59, 60, 61, 67],
    'Platform': [35, 40, 43, 51, 57, 60, 62, 63, 65, 66, 68],
    'Equipment' : [42, 44, 53, 69],
    'Helium': [39, 40, 61, 67 ],
    'Rooms' : [34, 36, 47, 48, 64, 69,]
}



def get_camera_rtsp_path(cam_id):
    # ! Unfortunately, needs to be hardcoded.
    
    if 34 <= int(cam_id) <= 43:
        return f"rtsp://alphacam:maxalpha@alphacam{cam_id}.cern.ch/stream1"
    elif 44 <= int(cam_id) <= 48:
        return f"rtsp://alphacam:Maxalpha@alphacam{cam_id}.cern.ch/stream1"
    elif int(cam_id) >= 50:
        return f"rtsp://alpha-admin:Nmt30smiAg$@alphacam{cam_id}.cern.ch/stream1"
    else:
        return None
    
# Global camera cache
CAMERA_INSTANCES = {}
CAMERA_LOCK = threading.Lock()



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class VideoCamera(object):
    def __init__(self, camera_rtsp):
        self.video = cv2.VideoCapture(camera_rtsp)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success or image is None:
            return b''
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()



# def create_layout(App: dash.Dash, Server: Flask) -> dash.html.Div:
    
    
@server.route('/video_feed/<cam_id>')
def video_feed(cam_id):
    rtsp_url = get_camera_rtsp_path(cam_id)
    if not rtsp_url:
        return "Camera not found", 404
    
    with CAMERA_LOCK:
        if cam_id not in CAMERA_INSTANCES:
            print(f"[INFO] Creating new VideoCamera for cam {cam_id}")
            CAMERA_INSTANCES[cam_id] = VideoCamera(rtsp_url)

    return Response(gen(CAMERA_INSTANCES[cam_id]),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(gen(VideoCamera(rtsp_url)),
    #                 mimetype='multipart/x-mixed-replace; boundary=frame')



dropdown_menu = dcc.Dropdown(
    id="camera-label-dropdown",
    options=[{"label": label, "value": label} for label in CAMS_LABELS.keys()],
    value=list(CAMS_LABELS.keys())[0],
    style={"width": "300px", "margin": "20px auto"}
)






import layouts
from pages import home_page, zone_page, platform_page

app.layout = layouts.main_layout.create_layout(app)

# home_page.layout.children = layouts.home_layout.create_layout(app, server)
# zone_page.layout.children = layouts.zone_layout.create_layout(app, server)
# platform_page.layout.children = layouts.platform_layout.create_layout(app, server)





# ! Will try to avoid this by directly opening specific feeds in speccific pages.
# @app.callback(
#     dash.Output("camera-mosaic", "children"),
#     [dash.Input("camera-label-dropdown", "value"),
#      dash.Input("interval-component", "n_intervals")
#         ]
# )
# def update_mosaic(selected_label):
    
#     # Close any opened cameras
    
#     # Shut down all open video feeds
#     print(f"Selected label: {selected_label}")
#     cam_ids = CAMS_LABELS.get(selected_label, [])
#     print(f"Camera IDs: {cam_ids}")
#     if not cam_ids:
#         return html.Div("No cameras found for this label.")
    
#     cards = [dbc.Col(camera_card(str(cam_id)), width=4) for cam_id in cam_ids]
#     print(f"Generated cards")
#     return dbc.Row(cards, justify="center")


# layout = html.Div(
#     [
#         html.H2("Camera Area", style={"textAlign": "center", "margin": "20px"}),
#         dropdown_menu,
#         html.Div(id="camera-mosaic"),
#         dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
#     ]
# )

# app.layout = layout

# if __name__ == '__main__':
#     threading.Thread(target=app.run).start()
#     server.run()

