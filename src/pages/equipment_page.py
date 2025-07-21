import dash
import layouts.equipment_layout

dash.register_page(__name__, path="/equipment")

layout = layouts.equipment_layout.create_layout(dash.get_app(), dash.get_app().server)