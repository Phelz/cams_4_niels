import dash

dash.register_page(__name__, path="/helium")
layout = dash.html.Div(id='helium_page_div', children=[])