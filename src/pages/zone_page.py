import dash

dash.register_page(__name__, path="/zone")
layout = dash.html.Div(id='zone_page_div', children=[])