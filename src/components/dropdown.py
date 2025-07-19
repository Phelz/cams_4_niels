
from dash import Dash, dcc



def render(App: Dash, dropdown_id: str, dropdown_options: list, default_value: str):
    
    return dcc.Dropdown(
        options=dropdown_options,
        value = default_value,
        id=dropdown_id,
    )


