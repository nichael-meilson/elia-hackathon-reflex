import reflex as rx

from ...views.data_product.container import data_product_container


def search_data_container():
    return rx.flex(
        rx.vstack(
            rx.hstack(
                rx.heading("Search Data", size="5"),
                rx.button("Create query"),
            ),
            data_product_container(),
        ),
        background_color="var(--gray-3)",
    )