import flet as ft

from breach_checker import is_pwned
from generator import generate_password
from validator import check_strength

from components.section_title import section_title
from components.toggle_row import toggle_row
from core.theme import Palette


class SecurityView:
    def __init__(self, page: ft.Page, colors: Palette):
        self.page = page
        self.colors = colors
        self.clipboard = ft.Clipboard()

        self.status_text = ft.Text(
            value="",
            color=colors.muted,
            size=12,
        )

        self.current_password = ft.Text(
            value="",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=colors.primary,
            font_family="Consolas",
            selectable=True,
        )

        self.strength_badge = ft.Text(
            color=colors.primary,
            weight=ft.FontWeight.BOLD,
            size=13,
        )

        self.breach_text = ft.Text(
            color=colors.muted,
            size=12,
        )

        self.length_value_text = ft.Text(
            "20",
            size=18,
            color=colors.primary,
            weight=ft.FontWeight.BOLD,
        )

        self.service_input = ft.TextField(
            label="Service",
            border_radius=12,
            bgcolor=colors.surface_high,
            border_color=colors.outline,
        )

        self.username_input = ft.TextField(
            label="Username / Email",
            border_radius=12,
            bgcolor=colors.surface_high,
            border_color=colors.outline,
        )

        self.save_pwd_input = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_radius=12,
            bgcolor=colors.surface_high,
            border_color=colors.outline,
        )

        self.saved_list = ft.ListView(
            expand=True,
            spacing=10,
        )

        self.uppercase_switch = ft.Switch(value=True)
        self.lowercase_switch = ft.Switch(value=True)
        self.number_switch = ft.Switch(value=True)
        self.symbol_switch = ft.Switch(value=True)
        self.phrase_switch = ft.Switch(value=False)

        self.length_slider = ft.Slider(
            min=8,
            max=64,
            divisions=56,
            value=20,
            active_color=colors.primary,
            inactive_color=colors.surface_highest,
        )
        self.min_numbers_value_text = ft.Text(
            "1",
            size=18,
            color=colors.primary,
            weight=ft.FontWeight.BOLD,
        )

        self.min_symbols_value_text = ft.Text(
            "1",
            size=18,
            color=colors.primary,
            weight=ft.FontWeight.BOLD,
        )

        self.min_numbers_slider = ft.Slider(
            min=0,
            max=25,
            divisions=25,
            value=1,
            active_color=colors.primary,
            inactive_color=colors.surface_highest,
        )

        self.min_symbols_slider = ft.Slider(
            min=0,
            max=25,
            divisions=25,
            value=1,
            active_color=colors.primary,
            inactive_color=colors.surface_highest,
        )

        self.min_numbers_slider.on_change = self.sync_numbers
        self.min_symbols_slider.on_change = self.sync_symbols

        self.number_switch.on_change = self.sync_number_toggle
        self.symbol_switch.on_change = self.sync_symbol_toggle
        
        self.length_slider.on_change = self.sync_length
            
    def sync_numbers(self, e=None) -> None:

        value = int(self.min_numbers_slider.value or 0)

        self.min_numbers_value_text.value = str(value)

        self.number_switch.value = value > 0
        self.sync_minimum_constraints()
        self.page.update()

    def sync_symbols(self, e=None) -> None:

        value = int(self.min_symbols_slider.value or 0)

        self.min_symbols_value_text.value = str(value)

        self.symbol_switch.value = value > 0
        self.sync_minimum_constraints()
        self.page.update()

    def sync_number_toggle(self, e=None) -> None:

        if not self.number_switch.value:
            self.min_numbers_slider.value = 0
            self.min_numbers_value_text.value = "0"

        elif self.min_numbers_slider.value == 0:
            self.min_numbers_slider.value = 1
            self.min_numbers_value_text.value = "1"

        self.page.update()

    def sync_symbol_toggle(self, e=None) -> None:

        if not self.symbol_switch.value:
            self.min_symbols_slider.value = 0
            self.min_symbols_value_text.value = "0"

        elif self.min_symbols_slider.value == 0:
            self.min_symbols_slider.value = 1
            self.min_symbols_value_text.value = "1"

        self.page.update()

    def snack(self, message: str) -> None:
        self.page.overlay.append(
            ft.SnackBar(
                content=ft.Text(message),
                open=True,
            )
        )
        self.page.update()
        self.page.update()

    def set_status(self, message: str, color: str | None = None) -> None:
        self.status_text.value = message
        self.status_text.color = color or self.colors.muted

    async def copy_text(self, value: str) -> None:
        await self.clipboard.set(value)
        self.snack("Copied to clipboard.")

    def update_strength_ui(self, strength: str) -> None:
        self.strength_badge.value = f"{strength} Strength"

        if strength == "Strong":
            self.strength_badge.color = self.colors.primary

        elif strength == "Medium":
            self.strength_badge.color = self.colors.warn

        else:
            self.strength_badge.color = self.colors.error

    def sync_length(self, e=None) -> None:
        self.length_value_text.value = str(int(self.length_slider.value or 20))
        self.page.update()
        
    def sync_minimum_constraints(self) -> None:

        uppercase_required = 1 if self.uppercase_switch.value else 0

        lowercase_required = 1 if self.lowercase_switch.value else 0

        numbers_required = (
            int(self.min_numbers_slider.value or 0) if self.number_switch.value else 0
        )

        if self.number_switch.value and numbers_required == 0:
            numbers_required = 1

        symbols_required = (
            int(self.min_symbols_slider.value or 0) if self.symbol_switch.value else 0
        )

        if self.symbol_switch.value and symbols_required == 0:
            symbols_required = 1

        total_minimum = (
            uppercase_required
            + lowercase_required
            + numbers_required
            + symbols_required
        )

        current_length = int(self.length_slider.value or 0)

        if total_minimum > current_length:
            self.length_slider.value = total_minimum

            self.length_value_text.value = str(total_minimum)

    def generate_password_ui(self, e=None) -> None:
        try:
            self.sync_minimum_constraints()
            self.page.update()
            pwd = generate_password(
                int(self.length_slider.value or 20),
                self.uppercase_switch.value,
                self.lowercase_switch.value,
                self.number_switch.value,
                self.symbol_switch.value,
            )

            self.current_password.value = pwd
            self.save_pwd_input.value = pwd

            strength = check_strength(pwd)
            self.update_strength_ui(strength)

            breaches = is_pwned(pwd)

            if breaches == -1:
                self.breach_text.value = "Breach API unavailable."
                self.breach_text.color = self.colors.warn

            elif breaches > 0:
                self.breach_text.value = f"Found in {breaches} breaches."
                self.breach_text.color = self.colors.error

            else:
                self.breach_text.value = "No known breaches detected."
                self.breach_text.color = self.colors.primary

            self.set_status(
                "Password generated.",
                self.colors.primary,
            )

        except ValueError as ex:
            self.set_status(str(ex), self.colors.error)

            self.current_password.value = ""
            self.save_pwd_input.value = ""
            self.strength_badge.value = ""
            self.breach_text.value = ""

        self.page.update()

    async def copy_current_password(self, e) -> None:
        if not self.current_password.value:
            self.set_status(
                "Generate a password first.",
                self.colors.warn,
            )

            self.page.update()
            return

        await self.copy_text(self.current_password.value)

    def build(self) -> ft.Container:
        hero_card = ft.Container(
            bgcolor=self.colors.surface,
            border_radius=20,
            border=ft.Border.all(1, self.colors.outline),
            padding=24,
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            section_title(
                                "Generated Key",
                                ft.Icons.TUNE,
                                self.colors,
                            ),
                            ft.Container(
                                bgcolor=self.colors.surface_high,
                                border_radius=999,
                                padding=ft.Padding.symmetric(
                                    vertical=6,
                                    horizontal=12,
                                ),
                                content=self.strength_badge,
                            ),
                        ],
                    ),
                    ft.Container(
                        bgcolor=self.colors.surface_high,
                        border_radius=18,
                        padding=18,
                        border=ft.Border.all(
                            1,
                            self.colors.surface_highest,
                        ),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    content=self.current_password,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.CONTENT_COPY,
                                            icon_color=self.colors.text,
                                            bgcolor=self.colors.surface,
                                            on_click=self.copy_current_password,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.AUTORENEW,
                                            icon_color=self.colors.on_primary_container,
                                            bgcolor=self.colors.primary,
                                            on_click=self.generate_password_ui,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.TASK_ALT,
                                            icon_color=self.colors.on_primary_container,
                                            bgcolor=self.colors.primary,
                                            on_click=self.generate_password_ui,
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ),
                    self.breach_text,
                ],
            ),
        )

        parameters_panel = ft.Container(
            col={"xs": 12, "lg": 7},
            bgcolor=self.colors.surface,
            border_radius=20,
            border=ft.Border.all(1, self.colors.outline),
            padding=20,
            content=ft.Column(
                spacing=16,
                controls=[
                    section_title(
                        "Parameters",
                        ft.Icons.TUNE,
                        self.colors,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Key Length",
                                color=self.colors.muted,
                                size=14,
                            ),
                            ft.Container(
                                bgcolor=self.colors.surface_high,
                                border_radius=14,
                                padding=ft.Padding.symmetric(
                                    vertical=8,
                                    horizontal=12,
                                ),
                                content=self.length_value_text,
                            ),
                        ],
                    ),
                    self.length_slider,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Minimum Numbers",
                                color=self.colors.muted,
                                size=14,
                            ),
                            ft.Container(
                                bgcolor=self.colors.surface_high,
                                border_radius=14,
                                padding=ft.Padding.symmetric(
                                    vertical=8,
                                    horizontal=12,
                                ),
                                content=self.min_numbers_value_text,
                            ),
                        ],
                    ),
                    self.min_numbers_slider,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                "Minimum Special",
                                color=self.colors.muted,
                                size=14,
                            ),
                            ft.Container(
                                bgcolor=self.colors.surface_high,
                                border_radius=14,
                                padding=ft.Padding.symmetric(
                                    vertical=8,
                                    horizontal=12,
                                ),
                                content=self.min_symbols_value_text,
                            ),
                        ],
                    ),
                    self.min_symbols_slider,
                ],
            ),
        )

        ingredients_panel = ft.Container(
            col={"xs": 12, "lg": 5},
            bgcolor=self.colors.surface,
            border_radius=20,
            border=ft.Border.all(1, self.colors.outline),
            padding=20,
            content=ft.Column(
                spacing=14,
                controls=[
                    section_title(
                        "Ingredients",
                        ft.Icons.EXTENSION,
                        self.colors,
                    ),
                    toggle_row(
                        "Uppercase (A-Z)",
                        "A",
                        self.uppercase_switch,
                        self.colors,
                    ),
                    toggle_row(
                        "Lowercase (a-z)",
                        "a",
                        self.lowercase_switch,
                        self.colors,
                    ),
                    toggle_row(
                        "Numbers (0-9)",
                        "#",
                        self.number_switch,
                        self.colors,
                    ),
                    toggle_row(
                        "Symbols (!@$)",
                        "!",
                        self.symbol_switch,
                        self.colors,
                    ),
                ],
            ),
        )
        analysis_panel = ft.Container(
            bgcolor=self.colors.surface,
            border_radius=24,
            border=ft.Border.all(1, self.colors.outline),
            padding=24,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(
                                ft.Icons.BAR_CHART,
                                color=self.colors.primary,
                                size=22,
                            ),
                            ft.Text(
                                "Password Analysis",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=self.colors.text,
                            ),
                        ],
                    ),
                    ft.Divider(
                        height=1,
                        color=self.colors.surface_highest,
                    ),
                    ft.ResponsiveRow(
                        run_spacing=16,
                        spacing=16,
                        controls=[
                            # Overall Score
                            ft.Container(
                                col={"xs": 12, "md": 6, "xl": 4},
                                bgcolor=self.colors.surface_high,
                                border_radius=20,
                                border=ft.Border.all(
                                    1,
                                    self.colors.surface_highest,
                                ),
                                padding=20,
                                content=ft.Column(
                                    spacing=14,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Overall Score",
                                                    size=13,
                                                    color=self.colors.muted,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.VERIFIED,
                                                    color=self.colors.primary,
                                                    size=18,
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            spacing=4,
                                            vertical_alignment=ft.CrossAxisAlignment.END,
                                            controls=[
                                                ft.Text(
                                                    "98",
                                                    size=40,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=self.colors.primary,
                                                ),
                                                ft.Text(
                                                    "/100",
                                                    color=self.colors.muted,
                                                    size=14,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "Extremely Strong",
                                            color=self.colors.primary,
                                            weight=ft.FontWeight.BOLD,
                                            size=14,
                                        ),
                                    ],
                                ),
                            ),
                            # Crack Time
                            ft.Container(
                                col={"xs": 12, "md": 6, "xl": 4},
                                bgcolor=self.colors.surface_high,
                                border_radius=20,
                                border=ft.Border.all(
                                    1,
                                    self.colors.surface_highest,
                                ),
                                padding=20,
                                content=ft.Column(
                                    spacing=16,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Crack Time",
                                                    size=13,
                                                    color=self.colors.muted,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.TIMER,
                                                    color=self.colors.secondary_container,
                                                    size=18,
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Brute Force",
                                                    color=self.colors.muted,
                                                    size=13,
                                                ),
                                                ft.Text(
                                                    "3.5e+12 Years",
                                                    color=self.colors.text,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=13,
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Dictionary",
                                                    color=self.colors.muted,
                                                    size=13,
                                                ),
                                                ft.Text(
                                                    "Centuries",
                                                    color=self.colors.text,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=13,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                            # Pattern Analysis
                            ft.Container(
                                col={"xs": 12, "md": 6, "xl": 4},
                                bgcolor=self.colors.surface_high,
                                border_radius=20,
                                border=ft.Border.all(
                                    1,
                                    self.colors.surface_highest,
                                ),
                                padding=20,
                                content=ft.Column(
                                    spacing=14,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Pattern Analysis",
                                                    size=13,
                                                    color=self.colors.muted,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.AUTO_GRAPH,
                                                    color=self.colors.secondary_container,
                                                    size=18,
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            spacing=8,
                                            controls=[
                                                ft.Container(
                                                    width=8,
                                                    height=8,
                                                    border_radius=999,
                                                    bgcolor=self.colors.primary,
                                                ),
                                                ft.Text(
                                                    "High Entropy",
                                                    color=self.colors.text,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=13,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "No sequential patterns or dates detected.",
                                            color=self.colors.muted,
                                            size=13,
                                        ),
                                    ],
                                ),
                            ),
                            # Feedback
                            ft.Container(
                                col={"xs": 12, "md": 6, "xl": 4},
                                bgcolor=self.colors.surface_high,
                                border_radius=20,
                                border=ft.Border.all(
                                    1,
                                    self.colors.surface_highest,
                                ),
                                padding=20,
                                content=ft.Column(
                                    spacing=12,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Feedback",
                                                    size=13,
                                                    color=self.colors.muted,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.INFO_OUTLINE,
                                                    color=self.colors.primary,
                                                    size=18,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "• Excellent character diversity.",
                                            color=self.colors.text,
                                            size=13,
                                        ),
                                        ft.Text(
                                            "• Length provides massive key space.",
                                            color=self.colors.text,
                                            size=13,
                                        ),
                                    ],
                                ),
                            ),
                            # Suggestions
                            ft.Container(
                                col={"xs": 12, "md": 6, "xl": 4},
                                bgcolor=self.colors.surface_high,
                                border_radius=20,
                                border=ft.Border.all(
                                    1,
                                    self.colors.surface_highest,
                                ),
                                padding=20,
                                content=ft.Column(
                                    spacing=14,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Suggestions",
                                                    size=13,
                                                    color=self.colors.muted,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.LIGHTBULB_OUTLINE,
                                                    color=self.colors.secondary_container,
                                                    size=18,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "Password is near optimal. Consider using a password manager to store it safely.",
                                            color=self.colors.text,
                                            size=13,
                                        ),
                                    ],
                                ),
                            ),
                            # Vulnerabilities
                            ft.Container(
                                col={"xs": 12, "md": 6, "xl": 4},
                                bgcolor=self.colors.surface_high,
                                border_radius=20,
                                border=ft.Border.all(
                                    1,
                                    self.colors.surface_highest,
                                ),
                                padding=20,
                                content=ft.Column(
                                    spacing=14,
                                    controls=[
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text(
                                                    "Vulnerabilities",
                                                    size=13,
                                                    color=self.colors.muted,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.SHIELD_OUTLINED,
                                                    color=self.colors.secondary_container,
                                                    size=18,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "No immediate structural weaknesses. Resistant to common rainbow table attacks.",
                                            color=self.colors.text,
                                            size=13,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )
        return ft.Container(
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=24,
                        content=ft.Column(
                            spacing=16,
                            controls=[
                                ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Row(
                                            spacing=8,
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.PETS,
                                                    color=self.colors.primary,
                                                    size=28,
                                                ),
                                                ft.Text(
                                                    "Pawsword Generator",
                                                    size=30,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=self.colors.text,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "Generate secure passwords and keep intruders paws-off.",
                                            color=self.colors.muted,
                                            size=13,
                                        ),
                                    ],
                                ),
                                hero_card,
                                ft.ResponsiveRow(
                                    controls=[
                                        parameters_panel,
                                        ingredients_panel,
                                        analysis_panel
                                    ]
                                ),
                                self.status_text,
                            ],
                        ),
                    )
                ],
            ),
        )

    def refresh(self) -> None:
        self.sync_length()
        self.generate_password_ui()