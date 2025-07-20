import dash

dash.register_page(__name__, path="/platform")
layout = dash.html.Div(id='platform_page_div', children=[])