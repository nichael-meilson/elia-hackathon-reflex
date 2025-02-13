import reflex as rx

from a_dplbckbgen_polaris_hackathon_reflex.views.data_product.stats import stats_ui
from a_dplbckbgen_polaris_hackathon_reflex.views.data_product.table import main_table
from a_dplbckbgen_polaris_hackathon_reflex.views.download.container import download_container

def _tabs_trigger(text: str, icon: str, value: str):
    return rx.tabs.trigger(
        rx.hstack(
            rx.icon(icon, size=24),
            rx.heading(text, size="5"),
            spacing="2",
            align="center",
            width="100%",
        ),
        value=value,
    )


def data_product_container():
    return rx.container(
        rx.hstack(
            rx.vstack(
                rx.link("Go back to Active Power Schedule", size="2"),
                rx.heading("Delivery point schedule", size="3"),
                rx.tabs.root(
                    rx.tabs.list(
                        _tabs_trigger("Preview Data", "table-2", value="table"),
                        _tabs_trigger("Overview", "bar-chart-3", value="stats"),
                        _tabs_trigger("Create Query", "table-2", value="table"),
                    ),
                    rx.tabs.content(
                        main_table(),
                        margin_top="1em",
                        value="table",
                    ),
                    rx.tabs.content(
                        stats_ui(),
                        margin_top="1em",
                        value="stats",
                    ),
                    default_value="table",
                    width="100%",
                ),
                width="100%",
                spacing="6",
                padding_x=["1.5em", "1.5em", "3em", "5em"],
                padding_y=["1.25em", "1.25em", "2em"],
            ),
            download_container(),
            background_color="var(--white-3)",

        ),
    )