import reflex as rx

from ...views.data_product.container import data_product_container


def search_data_container():
    return rx.container(
        rx.vstack(
            rx.heading("Search Data", size="5"),
            data_product_container(),
        ),
        rx.button("Create query"),
        background_color="var(--gray-3)",
    )