
from dash import Dash
import dash_bootstrap_components as dbc

import components


def render(App: Dash, button_name: str, button_id: str, color: str = "dark"):
    
    return dbc.Button(button_name, id=button_id, color=color, className="me-1")


