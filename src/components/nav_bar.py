from dash import Dash, html
import dash_bootstrap_components as dbc

import components


def render(App: Dash):
    
        
    home_tab  = dbc.NavItem(dbc.NavLink("Home", href="/"))
    
    zone_tab          = dbc.NavItem(dbc.NavLink("Zone", href="/zone"))
    platform_tab = dbc.NavItem(dbc.NavLink("Platform", href="/platform"))
    equipment_tab     = dbc.NavItem(dbc.NavLink("Equipment", href="/equipment"))
    helium_tab     = dbc.NavItem(dbc.NavLink("Helium", href="/helium"))
    rooms_tab     = dbc.NavItem(dbc.NavLink("Rooms", href="/rooms"))


    
    logo_row = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.NavbarBrand(App.title, className="ms-2"),
                ],
            ),
        ],
        align="start",
        className="flex-grow-1",
    )

    nav_bar_row = dbc.Row(
        dbc.Col(
            [
                dbc.Nav(
                    [
                        home_tab,
                        zone_tab,
                        platform_tab,
                        equipment_tab,
                        helium_tab,
                        rooms_tab,
                    ],
                    navbar=True,
                    pills=True,
                    className="ms-2",
                    id=components.ids.NAVBAR_ID,
                )
            ],
        ),
        align="start",
    )

    nav_bar = html.Div([dbc.Navbar(dbc.Container([logo_row, nav_bar_row]), color="dark", dark=True, sticky="top")])

    return nav_bar
