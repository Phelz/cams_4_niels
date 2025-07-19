
from dash import Dash, dcc
from datetime import datetime

import components

def render(App: Dash, min_date: datetime, max_date: datetime, default_date: datetime):

    date_picker = dcc.DatePickerSingle(
        id=components.ids.DAY_DATE_PICKER,
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        date=default_date,
        display_format='YYYY-MM-DD',
    )
    
    return date_picker