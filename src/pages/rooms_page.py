import dash
import layouts.rooms_layout
dash.register_page(__name__, path="/rooms")

layout = layouts.rooms_layout.create_layout(dash.get_app(), dash.get_app().server)