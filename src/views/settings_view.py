import flet as ft

from core.theme import Palette, THEMES


class SettingsView:
    def __init__(
        self,
        page: ft.Page,
        colors: Palette,
        current_theme: str,
        on_theme_change,
    ):
        self.page = page
        self.colors = colors
        self.current_theme = current_theme
        self.on_theme_change = on_theme_change

    def theme_card(
        self,
        theme_name: str,
        palette: Palette,
    ) -> ft.Container:

        is_active = theme_name == self.current_theme

        return ft.Container(
            width=260,
            border_radius=24,
            bgcolor=palette.surface,
            border=ft.Border.all(
                2 if is_active else 1,
                palette.primary if is_active else palette.outline,
            ),
            padding=20,
            ink=True,
            on_click=lambda e: self.on_theme_change(theme_name),
            content=ft.Column(
                spacing=18,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                theme_name.capitalize(),
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=palette.text,
                            ),
                            ft.Container(
                                width=14,
                                height=14,
                                border_radius=999,
                                bgcolor=palette.primary,
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            self.color_preview(palette.primary),
                            self.color_preview(palette.surface_high),
                            self.color_preview(palette.secondary_container),
                            self.color_preview(palette.background),
                        ],
                    ),
                    ft.Text(
                        "Currently Active"
                        if is_active
                        else "Click to apply theme",
                        color=palette.primary
                        if is_active
                        else palette.muted,
                        size=13,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        )

    def color_preview(self, color: str) -> ft.Container:
        return ft.Container(
            width=28,
            height=28,
            border_radius=999,
            bgcolor=color,
        )

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=32,
                        content=ft.Column(
                            spacing=28,
                            controls=[
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Text(
                                            "Settings",
                                            size=38,
                                            weight=ft.FontWeight.BOLD,
                                            color=self.colors.text,
                                        ),
                                        ft.Text(
                                            "Customize your PassCat experience and appearance.",
                                            color=self.colors.muted,
                                            size=15,
                                        ),
                                    ],
                                ),
                                ft.Container(
                                    bgcolor=self.colors.surface,
                                    border_radius=28,
                                    border=ft.Border.all(
                                        1,
                                        self.colors.outline,
                                    ),
                                    padding=28,
                                    content=ft.Column(
                                        spacing=24,
                                        controls=[
                                            ft.Row(
                                                spacing=12,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.PALETTE_OUTLINED,
                                                        color=self.colors.primary,
                                                        size=30,
                                                    ),
                                                    ft.Text(
                                                        "Themes",
                                                        size=28,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=self.colors.text,
                                                    ),
                                                ],
                                            ),
                                            ft.Text(
                                                "Choose a color palette for the application interface.",
                                                color=self.colors.muted,
                                            ),
                                            ft.ResponsiveRow(
                                                spacing=20,
                                                run_spacing=20,
                                                controls=[
                                                    ft.Container(
                                                        col={"xs": 12, "md": 6, "xl": 4},
                                                        content=self.theme_card(
                                                            name,
                                                            palette,
                                                        ),
                                                    )
                                                    for name, palette in THEMES.items()
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    bgcolor=self.colors.surface,
                                    border_radius=28,
                                    border=ft.Border.all(
                                        1,
                                        self.colors.outline,
                                    ),
                                    padding=28,
                                    content=ft.Column(
                                        spacing=14,
                                        controls=[
                                            ft.Row(
                                                spacing=12,
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.INFO_OUTLINE,
                                                        color=self.colors.primary,
                                                    ),
                                                    ft.Text(
                                                        "About Theming",
                                                        size=24,
                                                        weight=ft.FontWeight.BOLD,
                                                        color=self.colors.text,
                                                    ),
                                                ],
                                            ),
                                            ft.Text(
                                                "Themes are centrally managed in core/theme.py using palette objects.",
                                                color=self.colors.text,
                                            ),
                                            ft.Text(
                                                "You can add additional palettes by extending the THEMES dictionary.",
                                                color=self.colors.muted,
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )