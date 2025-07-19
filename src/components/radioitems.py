
from dash import Dash, dcc



def render(App: Dash, radioitems_id: str, radioitems_options: list, default_value: str, horizontal: bool = True):
    
    return dcc.RadioItems(
        options=radioitems_options,
        value = default_value,
        id=radioitems_id,
        inline=horizontal,
    )


