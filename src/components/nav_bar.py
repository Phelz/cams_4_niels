from dash import Dash, html
import dash_bootstrap_components as dbc

import components


def render(App: Dash):
    
    home_tab  = dbc.NavItem(dbc.NavLink("Home", href="/"))
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
                        # login_tab,
                        # database_tab,
                    ],
                    navbar=True,
                    id=components.ids.NAVBAR_ID,
                )
            ],
        ),
        align="start",
    )

    nav_bar = html.Div([dbc.Navbar(dbc.Container([logo_row, nav_bar_row]), color="dark", dark=True, sticky="top")])

    return nav_bar
