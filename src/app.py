from rich import print

import asyncio
import base64
import cv2
import threading

from quart import Quart, websocket, Response, send_from_directory
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import LUX as THEME

from collections import defaultdict
import time

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
    
# class VideoCamera(object):
#     def __init__(self, video_path):
#         self.video = cv2.VideoCapture(video_path)

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         success, image = self.video.read()
#         if not success:
#             print(f"[WARN] Failed to read frame from camera {self.video}")
#             return b''
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
class CameraStreamManager:
    def __init__(self):
        self.frames = {}  # cam_id -> latest frame (JPEG bytes)
        self.locks = defaultdict(threading.Lock) # thread-safe access to frames
        self.threads = {} # cam_id -> thread

    def start_camera_thread(self, cam_id: int, rtsp_url: str) -> None:
        ''' Start a thread to capture frames from the camera if not already started. '''
        
        if cam_id in self.threads:
            return

        def capture_loop():
            ''' Capture frames from the camera and update the frames dictionary. '''
            
            cap = cv2.VideoCapture(rtsp_url)
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    _, jpeg = cv2.imencode('.jpg', frame)
                    with self.locks[cam_id]:
                        self.frames[cam_id] = jpeg.tobytes()
                time.sleep(0.03)  # small time delay
        # Start the thread
        
        print(f"[INFO] Starting camera thread for {cam_id} with RTSP URL: {rtsp_url}")
        thread = threading.Thread(target=capture_loop, daemon=True)
        self.threads[cam_id] = thread
        thread.start()

    def get_frame(self, cam_id: int) -> bytes:
        ''' Get the latest frame for a given camera ID. '''
        with self.locks[cam_id]:
            return self.frames.get(cam_id, b'')

camera_manager = CameraStreamManager()

# Setup small Quart server for streaming via websocket.
server = Quart(__name__)
delay_between_frames = 0.05 # add delay (in seconds) if CPU usage is too high


# @server.websocket("/video_feed/<cam_id>")
# async def stream(cam_id):
#     camera = VideoCamera( get_camera_rtsp_path(cam_id) )  # zero means webcam
#     while True:
#         if delay_between_frames is not None:
#             await asyncio.sleep(delay_between_frames)  # add delay if CPU usage is too high
#         frame = camera.get_frame()
#         await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/video_feed/<cam_id>")
async def stream(cam_id):
    ''' Stream video frames for a given camera ID via WebSocket. Uses Asyncio for non-blocking I/O. '''
    cam_id = int(cam_id)
    rtsp_url = get_camera_rtsp_path(cam_id)
    camera_manager.start_camera_thread(cam_id, rtsp_url)

    while True:
        await asyncio.sleep(delay_between_frames)
        frame = camera_manager.get_frame(cam_id)
        if frame:
            await websocket.send(f"data:image/jpeg;base64,{base64.b64encode(frame).decode()}")



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

# Create a clientside callback for each camera to update the image source
# for key, cam_ids in CAMS_LABELS.items():
#     for cam_id in cam_ids:
#         app.clientside_callback(
#             f"function(m){{return m? m.data : '';}}",
#             Output(f"video-{cam_id}", "src"),
#             Input(f"ws-{cam_id}", "message")
#         )



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
