import dash

dash.register_page(__name__, path="/equipment")

layout = dash.html.Div(id='equipment_page_div', children=[])