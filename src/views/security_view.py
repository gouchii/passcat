import flet as ft

from breach_checker import is_pwned
from generator import generate_password
from validator import analyze_password

from components.section_title import section_title
from components.toggle_row import toggle_row
from core.theme import Palette


class SecurityView:
    def __init__(self, page: ft.Page, colors: Palette):
        self.page = page
        self.colors = colors
        self.clipboard = ft.Clipboard()
        self.analysis = None
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
            size=14,
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


        self.meter_bars = [
            ft.Container(
                expand=True, bgcolor=colors.surface_highest, border_radius=4, height=6
            ),
            ft.Container(
                expand=True, bgcolor=colors.surface_highest, border_radius=4, height=6
            ),
            ft.Container(
                expand=True, bgcolor=colors.surface_highest, border_radius=4, height=6
            ),
            ft.Container(
                expand=True, bgcolor=colors.surface_highest, border_radius=4, height=6
            ),
            ft.Container(
                expand=True, bgcolor=colors.surface_highest, border_radius=4, height=6
            ),
        ]

        self.strength_meter = ft.Row(spacing=4, controls=self.meter_bars)


        self.score_text = ft.Text(
            "--", size=48, weight=ft.FontWeight.BOLD, color=colors.primary
        )
        self.score_label = ft.Text(
            "Unknown", color=colors.primary, weight=ft.FontWeight.W_500, size=14
        )
        self.crack_time_bf = ft.Text(
            "--", color=colors.text, weight=ft.FontWeight.W_500, size=14
        )
        self.crack_time_dict = ft.Text(
            "--", color=colors.text, weight=ft.FontWeight.W_500, size=14
        )
        self.pattern_text = ft.Text(
            "--", color=colors.text, weight=ft.FontWeight.W_500, size=14
        )

        self.pattern_desc = ft.Text(
            "Awaiting analysis...",
            color=colors.muted,
            size=14,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.feedback_text = ft.Text(
            "--",
            color=colors.muted,
            size=14,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.suggestions_text = ft.Text(
            "--",
            color=colors.muted,
            size=14,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS,
        )
        self.vulnerabilities_text = ft.Text(
            "--",
            color=colors.muted,
            size=14,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS,
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

    def set_status(self, message: str, color: str | None = None) -> None:
        self.status_text.value = message
        self.status_text.color = color or self.colors.muted

    async def copy_text(self, value: str) -> None:
        await self.clipboard.set(value)
        self.snack("Copied to clipboard.")

    def update_strength_ui(self) -> None:
        if not self.analysis:
            self.strength_badge.value = "Unknown Strength"
            self.strength_badge.color = self.colors.muted
            for bar in self.meter_bars:
                bar.bgcolor = self.colors.surface_highest
            return

        score = self.analysis.get("score", 0)


        if score <= 1:
            color = self.colors.error
        elif score == 2:
            color = self.colors.warn
        else:
            color = self.colors.primary


        self.strength_badge.value = f"{self.score_label.value} Strength"
        self.strength_badge.color = color

        active_bars = score + 1
        for i, bar in enumerate(self.meter_bars):
            if i < active_bars:
                bar.bgcolor = color
            else:
                bar.bgcolor = self.colors.surface_highest

    def sync_length(self, e=None) -> None:
        self.length_value_text.value = str(int(self.length_slider.value or 20))
        self.page.update()

    def update_analysis_ui(self) -> None:
        if not self.analysis:
            self.score_text.value = "--"
            self.score_label.value = "Unknown"
            self.score_text.color = self.colors.primary
            self.score_label.color = self.colors.primary
            self.crack_time_bf.value = "--"
            self.crack_time_dict.value = "--"
            self.pattern_text.value = "--"
            self.pattern_desc.value = "Awaiting analysis..."
            self.feedback_text.value = "--"
            self.suggestions_text.value = "--"
            self.vulnerabilities_text.value = "--"
            return

        score = self.analysis.get("score", 0)
        self.score_text.value = str(score * 25)

        labels = {
            0: "Very Weak",
            1: "Weak",
            2: "Fair",
            3: "Strong",
            4: "Extremely Strong",
        }
        self.score_label.value = labels.get(score, "Unknown")


        if score <= 1:
            score_color = self.colors.error
        elif score == 2:
            score_color = self.colors.warn
        else:
            score_color = self.colors.primary

        self.score_text.color = score_color
        self.score_label.color = score_color

        crack_times = self.analysis.get("crack_times", {})
        self.crack_time_bf.value = str(
            crack_times.get("offline_fast_hashing_1e10_per_second", "--")
        )
        self.crack_time_dict.value = str(
            crack_times.get("offline_slow_hashing_1e4_per_second", "--")
        )

        seq = self.analysis.get("sequence", "")
        if isinstance(seq, list) and len(seq) > 0:
            raw_pattern = (
                str(seq[0].get("pattern", "None"))
                if isinstance(seq[0], dict)
                else str(seq[0])
            )
        else:
            raw_pattern = str(seq) if seq else "High Entropy"

        self.pattern_text.value = raw_pattern.replace("_", " ").title()

        if not seq or seq == "None" or seq == []:
            self.pattern_desc.value = "No sequential patterns or dates detected."
        else:
            self.pattern_desc.value = "Patterns detected in the password structure."

        feedback = self.analysis.get("feedback", {})
        suggestions = feedback.get("suggestions", [])
        warning = feedback.get("warning", "")

        if isinstance(suggestions, list) and suggestions:
            sugg_str = " ".join(suggestions)
        elif isinstance(suggestions, str) and suggestions:
            sugg_str = suggestions
        else:
            sugg_str = "Password is near optimal. Consider using a password manager to store it safely."

        self.feedback_text.value = warning if warning else "No major issues detected."
        self.suggestions_text.value = sugg_str
        self.vulnerabilities_text.value = (
            warning if warning else "No specific vulnerabilities detected."
        )

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
                int(self.min_numbers_slider.value or 0),
                int(self.min_symbols_slider.value or 0),
            )

            self.current_password.value = pwd


            self.analysis = analyze_password(pwd)

            self.update_analysis_ui()
            self.update_strength_ui()

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

    def _build_analysis_card(
        self, title: str, icon: str, icon_color: str, controls: list[ft.Control]
    ) -> ft.Container:
        return ft.Container(
            col={"xs": 12, "md": 6, "xl": 4},
            height=220,
            bgcolor=self.colors.surface_high,
            border_radius=24,
            border=ft.Border.all(1, self.colors.surface_highest),
            padding=24,
            content=ft.Column(
                spacing=16,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                title,
                                size=14,
                                color=self.colors.text,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Icon(icon, color=icon_color, size=20),
                        ],
                    ),
                    ft.Column(
                        spacing=12,
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        controls=controls,
                    ),
                ],
            ),
        )

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
                                    ]
                                ),
                            ],
                        ),
                    ),
                    self.strength_meter,
                    self.breach_text,
                ],
            ),
        )

        parameters_panel = ft.Container(
            col={"xs": 12, "lg": 7},
            bgcolor=self.colors.surface,
            border_radius=20,
            border=ft.Border.all(1, self.colors.outline),
            padding=24,
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
            padding=24,
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
            padding=32,
            content=ft.Column(
                spacing=24,
                controls=[
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Icon(
                                ft.Icons.BAR_CHART,
                                color=self.colors.primary,
                                size=24,
                            ),
                            ft.Text(
                                "Password Analysis",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=self.colors.text,
                            ),
                        ],
                    ),
                    ft.ResponsiveRow(
                        run_spacing=20,
                        spacing=20,
                        controls=[

                            self._build_analysis_card(
                                "Overall Score",
                                ft.Icons.VERIFIED,
                                self.colors.primary,
                                [
                                    ft.Row(
                                        spacing=8,
                                        vertical_alignment=ft.CrossAxisAlignment.END,
                                        controls=[
                                            self.score_text,
                                            ft.Text(
                                                "/ 100",
                                                color=self.colors.muted,
                                                size=14,
                                                weight=ft.FontWeight.W_500,
                                            ),
                                        ],
                                    ),
                                    self.score_label,
                                ],
                            ),

                            self._build_analysis_card(
                                "Crack Time",
                                ft.Icons.TIMER,
                                self.colors.secondary_container,
                                [
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                "Brute Force",
                                                color=self.colors.muted,
                                                size=14,
                                            ),
                                            self.crack_time_bf,
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                "Dictionary",
                                                color=self.colors.muted,
                                                size=14,
                                            ),
                                            self.crack_time_dict,
                                        ],
                                    ),
                                ],
                            ),

                            self._build_analysis_card(
                                "Pattern Analysis",
                                ft.Icons.AUTO_GRAPH,
                                self.colors.secondary_container,
                                [
                                    ft.Row(
                                        spacing=8,
                                        controls=[
                                            ft.Container(
                                                width=8,
                                                height=8,
                                                border_radius=999,
                                                bgcolor=self.colors.primary,
                                            ),
                                            self.pattern_text,
                                        ],
                                    ),
                                    self.pattern_desc,
                                ],
                            ),

                            self._build_analysis_card(
                                "Feedback",
                                ft.Icons.INFO_OUTLINE,
                                self.colors.primary,
                                [self.feedback_text],
                            ),

                            self._build_analysis_card(
                                "Suggestions",
                                ft.Icons.LIGHTBULB_OUTLINE,
                                self.colors.secondary_container,
                                [self.suggestions_text],
                            ),

                            self._build_analysis_card(
                                "Vulnerabilities",
                                ft.Icons.SHIELD_OUTLINED,
                                self.colors.secondary_container,
                                [self.vulnerabilities_text],
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
                        padding=32,
                        content=ft.Column(
                            spacing=24,
                            controls=[
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Row(
                                            spacing=12,
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.BUILD_CIRCLE,
                                                    color=self.colors.primary,
                                                    size=36,
                                                ),
                                                ft.Text(
                                                    "Password Forge",
                                                    size=32,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=self.colors.text,
                                                ),
                                            ],
                                        ),
                                        ft.Text(
                                            "Craft exceptionally strong, mathematically secure keys for your digital safe. Adjust the complexity below to fit your needs.",
                                            color=self.colors.muted,
                                            size=16,
                                        ),
                                    ],
                                ),
                                hero_card,
                                ft.ResponsiveRow(
                                    controls=[
                                        parameters_panel,
                                        ingredients_panel,
                                    ]
                                ),
                                analysis_panel,
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
