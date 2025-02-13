import reflex as rx
import reflex_chakra as rc

from ...views.data_product.container import data_product_container


def search_data_container():
    return rx.flex(
        rx.vstack(
            rx.hstack(
                rx.heading("Search Data", size="5"),
                rc.breadcrumb(
                    rc.breadcrumb_item(
                        rc.breadcrumb_link("Home", href="#")
                    ),
                    rc.breadcrumb_item(
                        rc.breadcrumb_link("Active Power Schedule", href="#")
                    ),
                    rc.breadcrumb_item(
                        rc.breadcrumb_link("Delivery Point Schedule", href="#")
                    ),
                ),
                rx.button("Create query"),
            ),
            data_product_container(),
        ),
        background_color="var(--gray-3)",
    )