import reflex as rx

from .views.download.container import download_container

from .backend.backend import State
from .views.navbar import navbar
from .views.data_product.container import data_product_container

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.heading("Search Data", size="5"),
        rx.hstack(
            data_product_container(),
            download_container()
        )
    )


base_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
    "grid.css",
]

base_style = {
    "font_family": "Inter",
}

app = rx.App(
    style=base_style,
    stylesheets=base_stylesheets,
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="orange"
    ),
)
app.add_page(
    index,
    on_load=State.load_entries,
    title="DataLink",
    description="NBA Data for the 2015-2016 season.",
)
