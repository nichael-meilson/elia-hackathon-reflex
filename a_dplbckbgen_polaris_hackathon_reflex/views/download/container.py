import reflex as rx

def _tabs_trigger(text: str, icon: str, value: str):
    return rx.tabs.trigger(
        rx.hstack(
            rx.icon(icon, size=10),
            rx.heading(text, size="2"),
            spacing="2",
            align="center",
            width="100%",
        ),
        value=value,
    )

def download_container():
    return rx.container(
        rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    _tabs_trigger("Export", "table-2", value="table"),
                    _tabs_trigger("API", "bar-chart-3", value="stats"),
                    _tabs_trigger("Python", "table-2", value="text"),
                ),
                rx.text("Download the selected data in CSV format."),
                rx.button("Export Data"),
                # rx.tabs.content(
                #     main_table(),
                #     margin_top="1em",
                #     value="table",
                # ),
                # rx.tabs.content(
                #     stats_ui(),
                #     margin_top="1em",
                #     value="stats",
                # ),
                # default_value="table",
                # width="100%",
            ),
        )
    )



