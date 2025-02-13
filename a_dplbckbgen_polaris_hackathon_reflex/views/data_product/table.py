import reflex as rx

from ...backend.backend import Job, State
from ...backend.data_items import position_dict, teams_dict
from ...components.item_badges import item_badge


def _header_cell(text: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_job(job: Job, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(job.scheduleid),
        rx.table.cell(job.version),
        rx.table.cell(job.date_utc),
        rx.table.cell(job.direction),
        rx.table.cell(job.power),
        rx.table.cell(job.deliverypoint),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(State.page_number),
                f" of {State.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=State.first_page,
                    opacity=rx.cond(State.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(State.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=State.prev_page,
                    opacity=rx.cond(State.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(State.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=State.next_page,
                    opacity=rx.cond(State.page_number == State.total_pages, 0.6, 1),
                    color_scheme=rx.cond(
                        State.page_number == State.total_pages, "gray", "accent"
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=State.last_page,
                    opacity=rx.cond(State.page_number == State.total_pages, 0.6, 1),
                    color_scheme=rx.cond(
                        State.page_number == State.total_pages, "gray", "accent"
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )


def main_table() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.cond(
                State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                [
                    "scheduleid",
                    "version",
                    "date_utc",
                    "direction",
                    "power",
                    "deliverypoint",
                ],
                placeholder="Sort By: Name",
                size="3",
                on_change=State.set_sort_value,
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                rx.input.slot(
                    rx.icon("x"),
                    justify="end",
                    cursor="pointer",
                    on_click=State.setvar("search_value", ""),
                    display=rx.cond(State.search_value, "flex", "none"),
                ),
                value=State.search_value,
                placeholder="Search here...",
                size="3",
                max_width="250px",
                width="100%",
                variant="surface",
                color_scheme="gray",
                on_change=State.set_search_value,
            ),
            align="center",
            justify="end",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("MwScheduleId"),
                    _header_cell("Version"),
                    _header_cell("VersionDate_UTC"),
                    _header_cell("Direction"),
                    _header_cell("Power"),
                    _header_cell("Delivery Point"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    State.get_current_page,
                    lambda job, index: _show_job(job, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
    )
