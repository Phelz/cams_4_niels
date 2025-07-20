import dash
dash.register_page(__name__, path="/rooms")
layout = dash.html.Div(id='rooms_page_div', children=[])