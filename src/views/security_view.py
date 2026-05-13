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
        self.is_at_bottom = False
        self.status_text = ft.Text(
            value="",
            color=colors.muted,
            size=12,
        )

        self.current_password = ft.TextField(
            value="",
            text_size=22,
            color=colors.primary,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD,
                font_family="Consolas",
            ),
            border=ft.InputBorder.NONE,
            bgcolor=ft.Colors.TRANSPARENT,
            content_padding=0,
            cursor_color=colors.primary,
            on_change=self.on_password_edit,
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
            "0",
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
            min=0,
            max=64,
            divisions=56,
            value=3,
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


        self.scroll_button = ft.FloatingActionButton(
            icon=ft.Icons.ARROW_DOWNWARD,
            bgcolor=colors.primary,
            on_click=self.toggle_scroll,
            tooltip="Scroll to Analysis",
        )

        self.min_numbers_slider.on_change = self.sync_numbers
        self.min_symbols_slider.on_change = self.sync_symbols

        self.number_switch.on_change = self.sync_number_toggle
        self.symbol_switch.on_change = self.sync_symbol_toggle

        self.length_slider.on_change = self.sync_length


    def handle_scroll(self, e: ft.OnScrollEvent) -> None:
        if e.max_scroll_extent <= 0:
            if self.scroll_button.visible:
                self.scroll_button.visible = False
                self.scroll_button.update()
            return

        if not self.scroll_button.visible:
            self.scroll_button.visible = True

        at_bottom = e.pixels >= (e.max_scroll_extent - 50)

        if at_bottom != self.is_at_bottom:
            self.is_at_bottom = at_bottom
            if self.is_at_bottom:
                self.scroll_button.icon = ft.Icons.ARROW_UPWARD
                self.scroll_button.tooltip = "Scroll to Top"
            else:
                self.scroll_button.icon = ft.Icons.ARROW_DOWNWARD
                self.scroll_button.tooltip = "Scroll to Analysis"
            self.scroll_button.update()

    async def toggle_scroll(self, e) -> None:
        """Fires when the scroll button is clicked. Uses universally supported offset parameter."""
        if self.is_at_bottom:
            await self.scroll_column.scroll_to(offset=0, duration=300)
        else:

            await self.scroll_column.scroll_to(offset=99999, duration=300)

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

    def on_password_edit(self, e) -> None:
        pwd = self.current_password.value

        if not pwd:
            self.analysis = None
            self.update_analysis_ui()
            self.update_strength_ui()
            self.breach_text.value = ""
            self.set_status("Awaiting input.", self.colors.muted)
            self.page.update()
            return

        try:
            self.analysis = analyze_password(pwd)
            self.update_analysis_ui()
            self.update_strength_ui()

            self.breach_text.value = (
                "Manual edit detected. Click refresh to check breaches."
            )
            self.breach_text.color = self.colors.muted

            self.set_status("Live analysis updated.", self.colors.primary)
        except Exception as ex:
            self.set_status(str(ex), self.colors.error)

        self.page.update()

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
        self.length_value_text.value = str(int(self.length_slider.value or 0))
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

        seq = self.analysis.get("sequence", [])

        meaningful_patterns = []
        if isinstance(seq, list):
            for item in seq:
                pattern_name = (
                    item.get("pattern", "") if isinstance(item, dict) else str(item)
                )
                if pattern_name and pattern_name != "bruteforce":
                    meaningful_patterns.append(pattern_name)

        primary_pattern = ""
        if not meaningful_patterns:
            self.pattern_text.value = "High Entropy"
            self.pattern_desc.value = (
                "No sequential patterns or dictionary words detected."
            )
        else:
            primary_pattern = meaningful_patterns[0].replace("_", " ")
            self.pattern_text.value = primary_pattern.title()
            self.pattern_desc.value = (
                f"Detected {primary_pattern} patterns in the structure."
            )

        feedback = self.analysis.get("feedback", {})
        suggestions = feedback.get("suggestions", [])
        warning = feedback.get("warning", "")

        if isinstance(suggestions, list) and suggestions:
            self.suggestions_text.value = " ".join(suggestions)
        elif isinstance(suggestions, str) and suggestions:
            self.suggestions_text.value = suggestions
        else:
            self.suggestions_text.value = "Password is near optimal. Consider using a password manager to store it safely."

        if warning:
            self.vulnerabilities_text.value = warning
        elif meaningful_patterns:
            self.vulnerabilities_text.value = f"Structure is potentially vulnerable to targeted {primary_pattern} attacks."
        else:
            self.vulnerabilities_text.value = "No specific vulnerabilities detected. Immune to standard dictionary attacks."

        if score >= 3:
            self.feedback_text.value = "Excellent character diversity. Length and entropy provide a massive key space."
        elif score == 2:
            self.feedback_text.value = "Moderate strength. Consider increasing length or adding special characters."
        else:
            self.feedback_text.value = "Weak structure. Highly recommended to use a longer phrase or more random characters."

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
                                padding=ft.Padding(left=12, top=6, right=12, bottom=6),
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
                                padding=ft.Padding(left=12, top=8, right=12, bottom=8),
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
                                padding=ft.Padding(left=12, top=8, right=12, bottom=8),
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
                                padding=ft.Padding(left=12, top=8, right=12, bottom=8),
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
            key="analysis_panel",
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
                                            ft.Container(
                                                padding=ft.Padding(
                                                    left=0, top=0, right=0, bottom=8
                                                ),
                                                content=ft.Text(
                                                    "/ 100",
                                                    color=self.colors.muted,
                                                    size=14,
                                                    weight=ft.FontWeight.W_500,
                                                ),
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

        self.scroll_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            on_scroll=self.handle_scroll,
            expand=True,
            controls=[
                ft.Container(
                    padding=32,
                    content=ft.Column(
                        spacing=24,
                        controls=[
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
        )

        return ft.Container(
            expand=True,
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Container(
                        left=0, right=0, top=0, bottom=0, content=self.scroll_column
                    ),
                    ft.Container(
                        bottom=32,
                        left=0,
                        right=0,
                        alignment=ft.Alignment(0, 0),
                        content=self.scroll_button,
                    ),
                ],
            ),
        )

    def refresh(self) -> None:
        self.sync_length()
        self.generate_password_ui()
