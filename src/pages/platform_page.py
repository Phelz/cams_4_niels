import dash

dash.register_page(__name__, path="/platform")
# layout = dash.html.Div(id='platform_page_div', children=[])

import layouts.platform_layout
layout = layouts.platform_layout.create_layout(dash.get_app(), dash.get_app().server)