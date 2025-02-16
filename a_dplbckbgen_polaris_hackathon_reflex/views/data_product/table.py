import reflex as rx
from reflex_ag_grid import ag_grid

from ...backend.backend import Job, State

def main_table() -> rx.Component:
    column_defs = [
        {"headerName": "MwScheduleId", "field": "scheduleid", "sortable": True, "filter": True},
        {"headerName": "Version", "field": "version", "sortable": True, "filter": True},
        {"headerName": "VersionDate_UTC", "field": "date_utc", "sortable": True, "filter": "agDateColumnFilter"},
        {"headerName": "Direction", "field": "direction", "sortable": True, "filter": True},
        {"headerName": "Power", "field": "power", "sortable": True, "filter": True},
        {"headerName": "Delivery Point", "field": "deliverypoint", "sortable": True, "filter": True},
    ]

    return rx.fragment(
        ag_grid(
            id="new-table",
            column_defs=column_defs,
            row_data=State.get_current_page,
            pagination=True,
            pagination_page_size=10,
            dom_layout="autoHeight",
            filter=True,
            sortable=True,
            resizable=True,
            style={"width": "100%"},
        )
    )
