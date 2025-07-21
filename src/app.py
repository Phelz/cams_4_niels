from rich import print

import asyncio
import base64
import cv2
import threading

from quart import Quart, websocket, Response, send_from_directory
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import LUX as THEME

# === DASH + QUART SETUP ===
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
    
class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            print(f"[WARN] Failed to read frame from camera {self.video}")
            return b''
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


# Setup small Quart server for streaming via websocket.
server = Quart(__name__)
delay_between_frames = 0.00  # add delay (in seconds) if CPU usage is too high


@server.websocket("/video_feed/<cam_id>")
async def stream(cam_id):
    camera = VideoCamera( get_camera_rtsp_path(cam_id) )  # zero means webcam
    while True:
        if delay_between_frames is not None:
            await asyncio.sleep(delay_between_frames)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")



# === DASH  ===
app = dash.Dash(
    __name__,
    # server=server,
    title="Cams 4 Niels",
    external_stylesheets=[THEME],
    use_pages=True,
    meta_tags=[
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"},
    ],
)




# Dash multipage container
import layouts.main_layout
import components
from pages import home_page, zone_page, platform_page
app.layout = layouts.main_layout.create_layout(app)


# # Register pages (example)
# home_page.layout = layouts.home_layout.create_layout(app, server)
# zone_page.layout = layouts.zone_layout.create_layout(app, server)
# platform_page.layout = layouts.platform_layout.create_layout(app, server)

# === RUN APP ===

if __name__ == "__main__":
    threading.Thread(target=app.run).start()
    server.run()
