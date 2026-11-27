import flet as ft
from .convert_bar import ConvertTab
from .history_bar import HistoryTab


class MainTabs:
    def __init__(self, page: ft.Page, colors: dict, theme_selected: str):
        self.page = page
        self.colors = colors
        self.convert_tab = ConvertTab(page, colors, theme_selected)
        self.history_tab = HistoryTab(page, colors, theme_selected)

    def build(self) -> ft.Tabs:
        return ft.Tabs(
            length=2,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.TabBar(
                                    splash_border_radius=ft.BorderRadius.only(top_left=30, top_right=30, bottom_left=10,
                                                                              bottom_right=10),
                                    indicator_size=ft.TabBarIndicatorSize.TAB,
                                    indicator=ft.UnderlineTabIndicator(
                                        border_radius=70,
                                        border_side=ft.BorderSide(2, self.colors["border"]),
                                    ),
                                    tabs=[
                                        ft.Tab(label="Конвертировать"),
                                        ft.Tab(label="История")
                                    ],
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            # 1. Вкладка Конвертировать (берем из ConvertTab)
                            self.convert_tab.build(),

                            # 2. Вкладка История (берем из HistoryTab)
                            self.history_tab.build()
                        ],
                    ),
                ]
            ),
        )