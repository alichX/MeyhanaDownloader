import json
import sys
from pathlib import Path

import flet as ft


def load_theme_data(path: str = "config/theme.json") -> dict:
    if getattr(sys, "frozen", False):
        config_path = Path(sys._MEIPASS) / "config" / "theme.json"
    else:
        config_path = Path(path)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_theme(page: ft.Page, theme_data: dict) -> tuple[str, dict]:
    selected = theme_data["selected"]
    colors = theme_data[selected]

    theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=colors["primary"],
            on_primary=colors["on_primary"],
            surface=colors["surface"],
            on_surface=colors["text"],
            on_surface_variant=colors["text_secondary"],
            outline=colors["border"],
            surface_container_highest=colors["input_bg"],
            surface_container=colors["card"],
        )
    )

    if selected == "dark":
        page.theme_mode = ft.ThemeMode.DARK
        page.dark_theme = theme
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = theme

    page.bgcolor = colors["background"]
    return selected, colors