import flet as ft

from core.theme import apply_theme
from components.sidebar import build_sidebar
from components.shell import AppShell

# Not implemented yet
# from services.vault_service import VaultService
# from views.auth.setup_view import SetupView
# from views.auth.unlock_view import UnlockView
from views.security_view import SecurityView
from views.settings_view import SettingsView


async def main(page: ft.Page):
    app_state = {"theme": "forest"}

    colors = apply_theme(page, app_state["theme"])

    page.title = "PassCat"
    page.window.width = 1400
    page.window.height = 900

    # Not implemented yet
    # vault = VaultService()
    def set_theme(theme_name: str):
        nonlocal colors, sidebar, security_view, settings_view

        app_state["theme"] = theme_name

        colors = apply_theme(page, theme_name)

        sidebar = build_sidebar(
            colors=colors,
            active_route=page.route,
            on_nav=lambda route: page.navigate(route),
        )

        security_view = SecurityView(page, colors)

        settings_view = SettingsView(
            page=page,
            colors=colors,
            current_theme=app_state["theme"],
            on_theme_change=set_theme,
        )

        shell.row.controls[0] = sidebar

        set_content(page.route)

        page.update()

    def placeholder_view(title: str) -> ft.Container:
        return ft.Container(
            expand=True,
            padding=32,
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Text(
                        title,
                        size=36,
                        weight=ft.FontWeight.BOLD,
                        color=colors.text,
                    ),
                    ft.Container(
                        padding=24,
                        border_radius=24,
                        bgcolor=colors.surface,
                        border=ft.Border.all(1, colors.outline),
                        content=ft.Text(
                            "UI placeholder view",
                            color=colors.muted,
                        ),
                    ),
                ],
            ),
        )

    content_area = ft.Container(expand=True)

    sidebar = build_sidebar(
        colors=colors,
        active_route="/app/security",
        on_nav=lambda route: page.navigate(route),
    )

    shell = AppShell(
        sidebar=sidebar,
        content_area=content_area,
    )
    security_view = SecurityView(page, colors)
    settings_view = SettingsView(
        page=page,
        colors=colors,
        current_theme=app_state["theme"],
        on_theme_change=set_theme,
    )
    def set_content(route: str) -> None:
        if route == "/app/settings":
            content_area.content = settings_view.build()

        elif route == "/app/vault":
            content_area.content = placeholder_view("Vault")

        elif route == "/app/categories":
            content_area.content = placeholder_view("Categories")
        else:
            #security_view.refresh()
            content_area.content = security_view.build()

    def route_change(e: ft.RouteChangeEvent):


        new_sidebar = build_sidebar(
            colors=colors,
            active_route=page.route,
            on_nav=lambda route: page.navigate(route),
        )

        shell.row.controls[0] = new_sidebar

        # update content area
        set_content(page.route)

        page.update()

    page.on_route_change = route_change

    page.add(shell)

    await page.push_route("/app/security")


if __name__ == "__main__":
    ft.run(main)