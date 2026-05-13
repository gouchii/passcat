import flet as ft

from core.theme import apply_theme
from views.security_view import SecurityView


async def main(page: ft.Page):

    theme = apply_theme(page, "forest")

    page.title = "PassCat"
    page.window.maximized = True

    security_view = SecurityView(
        page,
        theme,
    )

    security_view.refresh()

    page.add(
        security_view.build()
    )


if __name__ == "__main__":
    ft.run(main)