import dash
import layouts.zone_layout

dash.register_page(__name__, path="/zone")

layout = layouts.zone_layout.create_layout(dash.get_app(), dash.get_app().server)