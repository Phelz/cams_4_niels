
from dash import Dash, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

import components


def render(App: Dash,  slider_id: str, min_val: float, max_val: float, step: float, default_val: float, marks: dict, vertical: bool) -> dcc.Slider:
    
    alt_slider = dcc.Slider(id=slider_id,
                            min=min_val, max=max_val, step=step,
                            value=default_val,
                            tooltip={"placement": "top", "always_visible": True },
                            marks=marks,
                            updatemode='drag',
                            persistence=True,
                            persistence_type='session',
                            vertical=vertical)

    return alt_slider


# # withou marks
# def render(App: Dash,  slider_id: str, min_val: float, max_val: float, step: float, default_val: float) -> dcc.Slider:
    
#     alt_slider = dcc.Slider(id=slider_id,
#                             min=min_val, max=max_val, step=step,
#                             value=default_val,
#                             tooltip={"placement": "top", "always_visible": True },
#                             updatemode='drag',
#                             persistence=True,
#                             persistence_type='session')

#     return alt_slider
    

