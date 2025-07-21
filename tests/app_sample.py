import asyncio
import base64
import dash, cv2
import dash_html_components as html
import threading

from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket

from collections import defaultdict
import time

# class VideoCamera(object):
#     def __init__(self, video_path):
#         self.video = cv2.VideoCapture(video_path)

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         success, image = self.video.read()
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()


class CameraStreamManager:
    def __init__(self):
        self.frames = {}  # cam_id -> latest frame (JPEG bytes)
        self.locks = defaultdict(threading.Lock)
        self.threads = {}

    def start_camera_thread(self, cam_id, rtsp_url):
        if cam_id in self.threads:
            return

        def capture_loop():
            cap = cv2.VideoCapture(rtsp_url)
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    _, jpeg = cv2.imencode('.jpg', frame)
                    with self.locks[cam_id]:
                        self.frames[cam_id] = jpeg.tobytes()
                time.sleep(0.03)  # adjust as needed

        thread = threading.Thread(target=capture_loop, daemon=True)
        self.threads[cam_id] = thread
        thread.start()

    def get_frame(self, cam_id):
        with self.locks[cam_id]:
            return self.frames.get(cam_id, b'')

camera_manager = CameraStreamManager()

# Setup small Quart server for streaming via websocket.
server = Quart(__name__)
delay_between_frames = 0.00  # add delay (in seconds) if CPU usage is too high


# @server.websocket("/stream/<cam_id>")
# async def stream(cam_id):
#     camera = VideoCamera(f'rtsp://alphacam:maxalpha@alphacam{cam_id}.cern.ch/stream1')  # zero means webcam
#     while True:
#         if delay_between_frames is not None:
#             await asyncio.sleep(delay_between_frames)  # add delay if CPU usage is too high
#         frame = camera.get_frame()
#         await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/stream/<cam_id>")
async def stream(cam_id):
    cam_id = int(cam_id)
    rtsp_url = f'rtsp://alphacam:maxalpha@alphacam{cam_id}.cern.ch/stream1'
    camera_manager.start_camera_thread(cam_id, rtsp_url)

    while True:
        await asyncio.sleep(delay_between_frames)
        frame = camera_manager.get_frame(cam_id)
        if frame:
            await websocket.send(f"data:image/jpeg;base64,{base64.b64encode(frame).decode()}")

        


# Create small Dash application for UI.
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Img(style={'width': '40%', 'padding': 10}, id="video1"),
    html.Img(style={'width': '40%', 'padding': 10}, id="video2"),
    WebSocket(url=f"ws://127.0.0.1:5000/stream/41", id="ws1"),
    WebSocket(url=f"ws://127.0.0.1:5000/stream/37", id="ws2"),
])
# Copy data from websocket to Img element.
app.clientside_callback("function(m){return m? m.data : '';}", Output(f"video1", "src"), Input(f"ws1", "message"))

app.clientside_callback("function(m){return m? m.data : '';}", Output(f"video2", "src"), Input(f"ws2", "message"))

if __name__ == '__main__':
    threading.Thread(target=app.run).start()
    server.run()