import flet as ft

from theme import load_theme_data, apply_theme
from ui import create_title_bar, ConvertTab


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        page.window.resizable = False
        page.window.title_bar_hidden = True

        self.theme_data = load_theme_data()
        self.theme_selected, self.colors = apply_theme(page, self.theme_data)

        self.title_bar = create_title_bar(page)
        self.convert_tab = ConvertTab(page, self.colors, self.theme_selected)

        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    controls=[
                        self.title_bar,
                        self.convert_tab.build(),
                    ],
                    expand=True,
                ),
            )
        )