import flet as ft

from components.nav_button import nav_button
from core.theme import Palette

def build_sidebar(
    colors: Palette,
    active_route: str,
    on_nav,
) -> ft.Container:
    return ft.Container(
        width=280,
        bgcolor=colors.surface_lowest,
        padding=ft.Padding(20, 24, 20, 20),
        border=ft.Border.only(right=ft.BorderSide(1, colors.outline)),
        content=ft.Column(
            expand=True,
            spacing=24,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text(
                            "PassCat",
                            size=28,
                            color=colors.primary,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "The Purrfect Password Vault",
                            size=12,
                            color=colors.muted,
                        ),
                    ],
                ),
                ft.Column(
                    spacing=8,
                    controls=[
                        nav_button(
                            "Vault",
                            ft.Icons.LOCK_OUTLINE,
                            active_route == "/app/vault",
                            colors,
                            lambda e: on_nav("/app/vault"),
                        ),
                        nav_button(
                            "Categories",
                            ft.Icons.CATEGORY_OUTLINED,
                            active_route == "/app/categories",
                            colors,
                            lambda e: on_nav("/app/categories"),
                        ),
                        nav_button(
                            "Security",
                            ft.Icons.VERIFIED_USER,
                            active_route == "/app/security",
                            colors,
                            lambda e: on_nav("/app/security"),
                        ),
                        nav_button(
                            "Settings",
                            ft.Icons.SETTINGS_OUTLINED,
                            active_route == "/app/settings",
                            colors,
                            lambda e: on_nav("/app/settings"),
                        ),
                    ],
                ),
                ft.Container(expand=True),
                ft.Container(
                    border_radius=16,
                    bgcolor=colors.surface,
                    border=ft.Border.all(
                        1,
                        colors.outline,
                    ),
                    ink=True,
                    padding=ft.Padding(18, 14, 18, 14),
                    content=ft.Row(
                        spacing=14,
                        controls=[
                            ft.Container(
                                width=36,
                                height=36,
                                border_radius=12,
                                bgcolor=colors.surface_high,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Icon(
                                    ft.Icons.ADD,
                                    size=18,
                                    color=colors.primary,
                                ),
                            ),
                            ft.Column(
                                spacing=1,
                                controls=[
                                    ft.Text(
                                        "New Credential",
                                        size=14,
                                        weight=ft.FontWeight.W_500,
                                        color=colors.text,
                                    ),
                                    ft.Text(
                                        "Add to vault",
                                        size=11,
                                        color=colors.muted,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    border_radius=14,
                    ink=True,
                    padding=12,
                    content=ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(
                                ft.Icons.LOCK,
                                color=colors.muted,
                                size=20,
                            ),
                            ft.Text(
                                "Lock Vault",
                                color=colors.muted,
                                size=14,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

