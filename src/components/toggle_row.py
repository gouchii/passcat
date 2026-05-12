from core.theme import Palette
import flet as ft

def toggle_row(
    title: str,
    badge_text: str,
    switch: ft.Switch,
    colors: Palette,
) -> ft.Container:
    return ft.Container(
        bgcolor=colors.surface,
        border_radius=20,
        border=ft.Border.all(1, colors.outline),
        padding=16,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    spacing=14,
                    controls=[
                        ft.Container(
                            width=44,
                            height=44,
                            border_radius=22,
                            bgcolor="#2d3526",
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(
                                badge_text,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=colors.primary,
                            ),
                        ),
                        ft.Text(
                            title,
                            color=colors.text,
                        ),
                    ],
                ),
                switch,
            ],
        ),
    )