import dash
import flask
from quart import Quart, websocket
import cv2
from rich import print
# from datetime import datetime, timedelta
from dash_bootstrap_components.themes import LUX as THEME

# from src import definitions

# Configure the app
app = dash.Dash(
    __name__,
    # server=Quart(__name__),
    server=flask.Flask(__name__),
    title="Cams 4 Niels",
    external_stylesheets=[THEME],
    use_pages=True,
    meta_tags=[
        {"charset": "utf-8"},
        {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"},
    ],
)

server = app.server

# Setup pages
import layouts
from pages import home_page

app.layout = layouts.main_layout.create_layout(app)

home_page.layout.children = layouts.home_layout.create_layout(app, server)



