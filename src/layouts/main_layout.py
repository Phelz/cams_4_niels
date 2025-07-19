import dash
import dash_bootstrap_components as dbc

import components

from rich import print


def create_layout(App: dash.Dash) -> dash.html.Div:
    
    
    home_tab  = dbc.NavItem(dbc.NavLink("Home", href="/"))
    
    
    foot_index_tab          = dbc.NavItem(dbc.NavLink("Foot Function", href="/foot_function"))
    low_back_disability_tab = dbc.NavItem(dbc.NavLink("Low Back Disability", href="/low_back_disability"))
    neck_disability_tab     = dbc.NavItem(dbc.NavLink("Neck Disability", href="/neck_disability"))

    questionnaire_tabs = [ foot_index_tab, low_back_disability_tab, neck_disability_tab ]
    
    
    layout = dash.html.Div(
        [
            dash.dcc.Location(id="url", refresh=False),
            components.nav_bar.render(App),
            dash.html.Div(id="page-content", children=[]),
            dash.page_container,
        ]
    )


    return layout