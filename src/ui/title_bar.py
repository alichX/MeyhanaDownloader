import flet as ft


def create_title_bar(page: ft.Page) -> ft.WindowDragArea:
    return ft.WindowDragArea(
        content=ft.Container(
            content=ft.Row(
                [
                    ft.Text("MeyhanaConverter", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.REMOVE_ROUNDED,
                        on_click=lambda e: (
                            setattr(page.window, "minimized", True),
                            page.update(),
                        ),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE_ROUNDED,
                        tooltip="Закрыть",
                        on_click=page.window.close,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=1,
        ),
    )