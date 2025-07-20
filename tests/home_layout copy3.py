import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import components
import cv2



from flask import Flask, Response
import cv2
from dash import html
import dash_bootstrap_components as dbc

from rich import print

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
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()



def create_layout(App: dash.Dash, Server: Flask) -> dash.html.Div:
    
        
    @Server.route('/video_feed/<cam_id>')
    def video_feed(cam_id):
        rtsp_url = get_camera_rtsp_path(cam_id)
        if not rtsp_url:
            return "Camera not found", 404
        return Response(gen(VideoCamera(rtsp_url)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def camera_card(cam_id):
        return dbc.Card(
            [
                dbc.CardImg(src=f"/video_feed/{cam_id}", top=True, style={"height": "300px", "objectFit": "cover"}),
            ],
            style={"width": "22rem", "margin": "10px"},
        )

    # layout = dbc.Container(
    #     [
    #         html.H1("Webcam Feeds", style={"textAlign": "center", "margin": "20px"}),
    #         dbc.Row(
    #             [
    #                 dbc.Col(camera_card("41")),
    #                 dbc.Col(camera_card("35")),
    #                 dbc.Col(camera_card("56")),
    #             ],
    #             justify="center",
    #         ),
    #     ],
    #     fluid=True,
    # )
    
    dropdown_menu = dcc.Dropdown(
        id="camera-label-dropdown",
        options=[{"label": label, "value": label} for label in CAMS_LABELS.keys()],
        value=list(CAMS_LABELS.keys())[0],
        style={"width": "300px", "margin": "20px auto"}
    )

    layout = html.Div(
        [
            html.H2("Camera Area", style={"textAlign": "center", "margin": "20px"}),
            dropdown_menu,
            html.Div(id="camera-mosaic"),
            # dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
        ]
    )

    @App.callback(
        dash.Output("camera-mosaic", "children"),
        [dash.Input("camera-label-dropdown", "value"),
        #  dash.Input("interval-component", "n_intervals")
         ]
    )
    # def update_mosaic(selected_label, n_intervals):
    def update_mosaic(selected_label):
        cam_ids = CAMS_LABELS.get(selected_label, [])
        if not cam_ids:
            return html.Div("No cameras found for this label.")
        cards = [dbc.Col(camera_card(str(cam_id)), width=4) for cam_id in cam_ids]
        return dbc.Row(cards, justify="center")
    
    return layout











# def get_camera_stream(cam_num: int):
#     print(f'Opening Stream for Cam # {cam_num:2d}')

#     # open a video stream
#     cap = cv2.VideoCapture(f"rtsp://alphacam:maxalpha@alphacam{cam_num:2d}.cern.ch/stream1") 
    
#     w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#     h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#     fps = cap.get(cv2.CAP_PROP_FPS)

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     print(f'Successfully Opened Stream for Cam # {cam_num:2d}')

#     return {
#         'capture': cap,
#         'width': w,
#         'height': h,
#         'fps': fps,
#         'fourcc': fourcc
#     }
    
# conf_room_stream = get_camera_stream(CAMS_LABELS['Conference Room'][0])
# print(f'Conference Room Stream: {conf_room_stream}')

# zone_room_stream = get_camera_stream(CAMS_LABELS['Zone'][0])
# print(f'Zone Room Stream: {zone_room_stream}')
    

# class VideoCamera(object):
#     def __init__(self, video_path):
#         self.video = cv2.VideoCapture(video_path)

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         success, image = self.video.read()

#         # Recolor image to RGB
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image.flags.writeable = False

#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()


# def create_layout(App: dash.Dash) -> dash.html.Div:

#     dropdown_menu = components.dropdown.render(
#         App,
#         dropdown_id=components.ids.CAMERA_DROPDOWN_ID,
#         dropdown_options=[
#             {'label': label, 'value': label} for label in CAMS_LABELS.keys()
#         ],
#         default_value='Zone',
#     )
    
#     layout = dash.html.Div(
#         id="foot-function-index-div",
#         children=[
#             dbc.Card(
#                 [
#                     dbc.CardHeader("Camera area:", className="card-title", style={"font-size": "2rem"}),

#                     dbc.CardBody(
#                         [
#                             dropdown_menu,
#                             dash.html.Div(id=components.ids.CAMERA_DROPDOWN_OUTPUT_ID, children=[]),
#                         ],
#                     ),
#                 ],
#                 style={"width": "80%", "margin": "auto", "margin-top": "20px", "margin-bottom": "20px"},
#             ),
#         ],
#     )

#     @App.callback(
#         dash.Output(components.ids.CAMERA_DROPDOWN_OUTPUT_ID, "children"),
#         [dash.Input(components.ids.CAMERA_DROPDOWN_ID, "value"),
#          dash.Input("interval-component", "n_intervals")]
#     )
#     def update_camera_feed(selected_label, n_intervals):
#         cam_num = CAMS_LABELS[selected_label][0]
#         print(f'Obtaining Feed for Cam # {cam_num:2d}')
#         stream = get_camera_stream(cam_num)
#         cap = stream['capture']
#         success, frame = cap.read()
#         if not success:
#             return dash.html.Div("Unable to fetch camera feed.")
#         # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         _, buffer = cv2.imencode('.jpg', frame)
#         img_base64 = base64.b64encode(buffer).decode('utf-8')
#         img_src = f"data:image/jpeg;base64,{img_base64}"
#         return dash.html.Img(src=img_src, style={"width": "100%", "height": "auto"})

#     # Add an interval component to trigger the callback every second
#     layout.children[0].children[1].children.append(
#         dash.dcc.Interval(id="interval-component", interval=1000, n_intervals=0)
#     )

#     return layout
