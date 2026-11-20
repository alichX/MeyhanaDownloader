import os
import asyncio
import flet as ft

from modules.downloader import get_video_info, download_video
from .video_card import create_video_card


class ConvertTab:
    def __init__(self, page: ft.Page, colors: dict, theme_selected: str):
        self.page = page
        self.colors = colors
        self.theme_selected = theme_selected

        self.correctly_info: dict | None = None
        self.cards_list: ft.ListView | None = None

        self.url_input = ft.TextField(
            border_radius=30,
            multiline=True,
            max_lines=10,
            width=500,
            text_align=ft.TextAlign.CENTER,
            on_blur=self._load_video_info,
        )

        self.info_count = ft.Text(margin=ft.Margin.only(top=15, left=6))

        self.info_progress = ft.Container(
            margin=10,
            bgcolor=colors["card"],
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=3, color=ft.Colors.GREY),
            content=ft.ProgressRing(margin=7),
            width=30,
            height=30,
            border_radius=50,
            visible=False,
        )

        self.download_progress = ft.ProgressRing(width=160, height=160, visible=False)

        self.convert_button = ft.Button(
            on_click=self._download,
            content=ft.Text("Скачать", size=16),
            height=150,
            width=150,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=0,
                alignment=ft.Alignment.CENTER,
            ),
            disabled=True,
        )

        self.format_switcher = ft.SegmentedButton(
            selected=["MP3"],
            allow_multiple_selection=False,
            segments=[
                ft.Segment(value="MP4", label=ft.Text("MP4")),
                ft.Segment(value="MP3", label=ft.Text("MP3")),
            ],
        )

        self.video_passport = ft.Container(expand=10)

        self.left_half_stack = ft.Stack(
            expand=10,
            controls=[self.video_passport, self.info_progress],
        )

    def build(self) -> ft.Tabs:
        return ft.Tabs(
            length=2,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.TabBar(
                            indicator=ft.UnderlineTabIndicator(
                                border_radius=70,
                                border_side=ft.BorderSide(2, self.colors["border"]),
                            ),
                            tabs=[
                                ft.Tab(label="Конвертировать"),
                            ],
                        )
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.left_half_stack,
                                        ft.Stack(
                                            expand=8,
                                            controls=[
                                                ft.Column(
                                                    alignment=ft.CrossAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        self.url_input,
                                                        ft.Stack(
                                                            alignment=ft.Alignment.CENTER,
                                                            controls=[
                                                                self.download_progress,
                                                                self.convert_button,
                                                            ],
                                                        ),
                                                        self.format_switcher,
                                                        ft.Container(
                                                            alignment=ft.Alignment.BOTTOM_RIGHT,
                                                            content=ft.IconButton(
                                                                icon=ft.Icons.FOLDER_ROUNDED,
                                                                on_click=self._open_downloads,
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                                self.info_count,
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ]
            ),
        )

    async def _load_video_info(self, e):
        self.convert_button.disabled = True
        self.info_progress.visible = True
        self.page.update()
        await asyncio.sleep(0)

        urls = e.control.value.splitlines()
        format_ = self.format_switcher.selected[0]

        correctly_info = await get_video_info(urls, format_)
        if not correctly_info:
            self.convert_button.disabled = False
            self.info_progress.visible = False
            self.page.update()
            return

        self.correctly_info = correctly_info
        self.cards_list = ft.ListView(expand=True, margin=ft.Margin.only(top=25))

        for key, info in correctly_info.items():
            card = create_video_card(
                key=key,
                info=info,
                colors=self.colors,
                on_delete=self._delete_card,
            )
            self.cards_list.controls.append(card)

        self.info_count.value = str(len(self.correctly_info))
        self.video_passport.content = self.cards_list
        self.info_progress.visible = False
        self.convert_button.disabled = False
        self.page.update()

    def _delete_card(self, key: str, card: ft.Container):
        words = [w for w in self.url_input.value.split() if w != key]
        self.url_input.value = " ".join(words)

        if self.correctly_info and key in self.correctly_info:
            del self.correctly_info[key]

        if self.cards_list and card in self.cards_list.controls:
            self.cards_list.controls.remove(card)

        current = int(self.info_count.value or 0)
        self.info_count.value = str(max(0, current - 1))
        self.page.update()

    async def _download(self, e):
        self.convert_button.disabled = True
        self.download_progress.visible = True
        self.convert_button.content = ft.Text("Скачивание...", size=16)
        self.page.update()
        await asyncio.sleep(0)

        try:
            await asyncio.to_thread(
                download_video,
                self.format_switcher.selected[0],
            )
        except Exception as ex:
            print(f"Ошибка: {ex}")
        finally:
            self.convert_button.content = ft.Text("Скачать", size=16)
            self.download_progress.visible = False
            self.convert_button.disabled = False
            self.page.update()

    def _open_downloads(self, e):
        if os.name == "nt":
            os.startfile("downloads")
        else:
            import subprocess
            import sys

            folder = os.path.abspath("downloads")
            if sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])