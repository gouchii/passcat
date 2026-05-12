from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class Palette:
    primary: str
    background: str
    surface_lowest: str
    surface: str
    surface_high: str
    surface_highest: str
    text: str
    muted: str
    outline: str
    primary_container: str
    on_primary_container: str
    secondary_container: str
    on_secondary_container: str
    error: str
    warn: str


THEMES: dict[str, Palette] = {
    "forest": Palette(
        primary="#bacd9b",
        background="#121410",
        surface_lowest="#0d0f0b",
        surface="#1a1c18",
        surface_high="#292b26",
        surface_highest="#333531",
        text="#e3e3dc",
        muted="#c5c8bb",
        outline="#45483e",
        primary_container="#859769",
        on_primary_container="#1f2e0a",
        secondary_container="#503f79",
        on_secondary_container="#c2aef0",
        error="#ffb4ab",
        warn="#ffb74d",
    ),
    "midnight": Palette(
        primary="#9cc3ff",
        background="#0f1218",
        surface_lowest="#0b0e13",
        surface="#151922",
        surface_high="#202635",
        surface_highest="#2a3142",
        text="#edf2ff",
        muted="#c5d0e6",
        outline="#3a4354",
        primary_container="#4a638f",
        on_primary_container="#eaf2ff",
        secondary_container="#4b3f78",
        on_secondary_container="#d9caff",
        error="#ffb4ab",
        warn="#ffd180",
    ),
    "amoled": Palette(
        primary="#7ee787",
        background="#000000",
        surface_lowest="#000000",
        surface="#050505",
        surface_high="#0a0a0a",
        surface_highest="#151515",
        text="#f5f5f5",
        muted="#b0b0b0",
        outline="#222222",
        primary_container="#1f3b2a",
        on_primary_container="#d7ffe2",
        secondary_container="#303050",
        on_secondary_container="#d0d0ff",
        error="#ffb4ab",
        warn="#ffd180",
    ),
}


def build_theme(colors: Palette) -> ft.Theme:
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=colors.primary,
            on_primary=colors.on_primary_container,
            primary_container=colors.primary_container,
            on_primary_container=colors.on_primary_container,
            secondary=colors.secondary_container,
            on_secondary=colors.on_secondary_container,
            secondary_container=colors.secondary_container,
            on_secondary_container=colors.on_secondary_container,
            surface=colors.surface,
            on_surface=colors.text,
            error=colors.error,
            outline=colors.outline,
        )
    )


def apply_theme(page: ft.Page, theme_name: str = "forest") -> Palette:
    colors = THEMES.get(theme_name, THEMES["forest"])

    page.theme_mode = ft.ThemeMode.DARK
    page.theme = build_theme(colors)
    page.dark_theme = build_theme(colors)
    page.bgcolor = colors.background
    page.padding = 0

    return colors