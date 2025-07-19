# import dash
# import flask
# from quart import Quart, websocket
# import cv2
# from rich import print
# # from datetime import datetime, timedelta
# from dash_bootstrap_components.themes import LUX as THEME

# # from src import definitions

# # Configure the app
# app = dash.Dash(
#     __name__,
#     # server=Quart(__name__),
#     server=flask.Flask(__name__),
#     title="Cams 4 Niels",
#     external_stylesheets=[THEME],
#     use_pages=True,
#     meta_tags=[
#         {"charset": "utf-8"},
#         {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"},
#     ],
# )



# # Setup pages
# import layouts
# from pages import home_page

# app.layout = layouts.main_layout.create_layout(app)

# home_page.layout.children = layouts.home_layout.create_layout(app)




import dash
from dash import dcc, html

from flask import Flask, Response
import cv2

class VideoCamera(object):
    def __init__(self, camera_rtsp):
        self.video = cv2.VideoCapture(camera_rtsp)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera("rtsp://alphacam:maxalpha@alphacam41.cern.ch/stream1")),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.layout = html.Div([
    html.H1("Webcam Test"),
    html.Img(src="/video_feed")
])

# if __name__ == '__main__':
#     app.run_server(debug=True)





# # top of the file
# import sys, asyncio

# if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# import asyncio
# import base64
# import dash, cv2
# from dash import html
# import threading

# from dash.dependencies import Output, Input
# from quart import Quart, websocket
# from dash_extensions import WebSocket
# import dash_bootstrap_components as dbc


# class VideoCamera(object):
#     def __init__(self, video_path):
#         self.video = cv2.VideoCapture(video_path)

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#     #     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         success, image = self.video.read()

#         # Recolor image to RGB
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#             # # Make detection
#             # results = pose.process(image)

#             # # Recolor back to BGR
#             # image.flags.writeable = True
#             # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             # # Render detections
#             # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#             #                           mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#             #                           mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
#             #                           )

#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()


# # Setup small Quart server for streaming via websocket, one for each stream.
# server = Quart(__name__)
# n_streams = 2


# async def stream(camera, delay=None):
#     while True:
#         if delay is not None:
#             await asyncio.sleep(delay)  # add delay if CPU usage is too high
#         frame = camera.get_frame()
#         await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


# @server.websocket("/stream0")
# async def stream0():
#     camera = VideoCamera("1.mp4")
#     await stream(camera)


# @server.websocket("/stream1")
# async def stream1():
#     camera = VideoCamera("2.mp4")
#     await stream(camera)


# # Create small Dash application for UI.
# app = dash.Dash(__name__)
# app.layout = html.Div(
#     children=[
#     html.H1("Camera Streams", style={'textAlign': 'center', 'padding': 20}),
#     [html.Img(style={'width': '40%', 'padding': 10}, id=f"v{i}") for i in range(n_streams)] +
#     [WebSocket(url=f"ws://127.0.0.1:5000/stream{i}", id=f"ws{i}") for i in range(n_streams)],
#     # html.Div(id="ws-output", style={'display': 'none'}),
#     ]
    
# )
# # Copy data from websockets to Img elements.
# for i in range(n_streams):
#     app.clientside_callback("function(m){return m? m.data : '';}", Output(f"v{i}", "src"), Input(f"ws{i}", "message"))

# if __name__ == '__main__':
#     threading.Thread(target=app.run).start()
#     server.run()
    
    
#     print("Server is running") 
    