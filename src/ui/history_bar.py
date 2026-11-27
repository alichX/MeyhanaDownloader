import flet as ft

class HistoryTab:
    def __init__(self, page: ft.Page, colors: dict, theme_selected: str):
        self.page = page
        self.colors = colors
        self.theme_selected = theme_selected
    def build(self) -> ft.Container:
        return ft.Container(
                    border_radius=30,
                    bgcolor="#F9D9B5",

                    expand=1,
                )
