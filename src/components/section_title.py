from core.theme import Palette
import flet as ft

def section_title(text: str, icon, colors: Palette) -> ft.Row:
    return ft.Row(
        spacing=10,
        controls=[
            ft.Icon(icon, color=colors.primary),
            ft.Text(
                text,
                size=24,
                weight=ft.FontWeight.BOLD,
                color=colors.text,
            ),
        ],
    )