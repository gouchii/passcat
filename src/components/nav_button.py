from core.theme import Palette
import flet as ft


def nav_button(
    label: str,
    icon,
    active: bool,
    colors: Palette,
    on_click,
) -> ft.Container:

    return ft.Container(
        border_radius=16,
        ink=True,
        bgcolor=(
            colors.primary_container
            if active
            else "transparent"
        ),
        content=ft.ListTile(
            leading=ft.Icon(
                icon,
                size=24,
                color=(
                    colors.on_primary_container
                    if active
                    else colors.muted
                ),
            ),
            title=ft.Text(
                label,
                size=15,
                weight=ft.FontWeight.W_500,
                color=(
                    colors.on_primary_container
                    if active
                    else colors.text
                ),
            ),
            content_padding=ft.Padding(
                left=18,
                top=6,
                right=12,
                bottom=6,
            ),
            horizontal_spacing=14,
        ),
        on_click=on_click,
    )