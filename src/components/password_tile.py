from core.theme import Palette
import flet as ft

def password_tile(
    service: str,
    username: str,
    on_copy,
    colors: Palette,
) -> ft.Container:
    return ft.Container(
        bgcolor=colors.surface_high,
        border_radius=20,
        border=ft.Border.all(1, colors.outline),
        padding=16,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=2,
                    expand=True,
                    controls=[
                        ft.Text(service, color=colors.text, weight=ft.FontWeight.BOLD),
                        ft.Text(username, color=colors.muted),
                    ],
                ),
                ft.IconButton(
                    icon=ft.Icons.COPY,
                    icon_color=colors.primary,
                    bgcolor=colors.surface,
                    on_click=on_copy,
                ),
            ],
        ),
    )
