import dash
import dash_bootstrap_components as dbc

import components

from rich import print


def create_layout(App: dash.Dash) -> dash.html.Div:
    
 
    
    layout = dash.html.Div(
        [
            dash.dcc.Location(id="url", refresh=False),
            components.nav_bar.render(App),
            dash.html.Div(id="page-content", children=[]),
            dash.page_container,
        ]
    )


    return layout