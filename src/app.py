import asyncio
import base64
import cv2
import threading
import dash
import time

from quart import Quart, websocket
from dash_bootstrap_components.themes import LUX as THEME
from collections import defaultdict
from rich import print

import config

class CameraStreamManager:
    ''' Manages camera streams and frames in a thread-safe manner. '''
    
    def __init__(self):
        ''' Initialize the camera stream manager. '''
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


# Setup small Quart server for streaming via websocket.
server = Quart(__name__) 
camera_manager = CameraStreamManager()

@server.websocket("/video_feed/<cam_id>")
async def stream(cam_id: int) -> None:
    ''' Stream video frames for a given camera ID via WebSocket. Uses Asyncio for non-blocking I/O. '''
    
    cam_id = int(cam_id)
    rtsp_url = config.get_camera_rtsp_path(cam_id)
    camera_manager.start_camera_thread(cam_id, rtsp_url)

    # The loop that sends frames to the WebSocket client
    while True:
        await asyncio.sleep(config.DELAY_BETWEEN_FRAMES) # Wait for the camera to have a frame ready
        frame = camera_manager.get_frame(cam_id)
        if frame:
            await websocket.send(f"data:image/jpeg;base64,{base64.b64encode(frame).decode()}")


# UI for displaying the camera feeds
app = dash.Dash(
    __name__,
    title="Cams 4 Niels",
    external_stylesheets=[THEME],
    use_pages=True,
    meta_tags=[
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"},
    ],
)

import layouts.main_layout
app.layout = layouts.main_layout.create_layout(app)

if __name__ == "__main__":
    threading.Thread(target=app.run).start()
    server.run()
