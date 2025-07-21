import dash
import layouts.helium_layout

dash.register_page(__name__, path="/helium")

layout = layouts.helium_layout.create_layout(dash.get_app(), dash.get_app().server)