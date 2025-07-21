import dash
import layouts.platform_layout

dash.register_page(__name__, path="/platform")

layout = layouts.platform_layout.create_layout(dash.get_app(), dash.get_app().server)