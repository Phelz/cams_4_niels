import dash

dash.register_page(__name__, path="/zone")
# layout = dash.html.Div(id='zone_page_div', children=[])

import layouts.zone_layout

layout = layouts.zone_layout.create_layout(dash.get_app(), dash.get_app().server)