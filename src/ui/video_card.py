import flet as ft


def create_video_card(
    key: str,
    info: tuple,
    colors: dict,
    on_delete,
) -> ft.Container:
    title, thumbnail, author, duration = info

    minutes = duration // 60
    seconds = duration % 60
    duration_str = f"{minutes}:{seconds:02d}"

    card = ft.Container(
        expand=True,
        aspect_ratio=16 / 7,
        margin=20,
        border_radius=45,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.GREY),
        bgcolor=colors["card"],
        content=ft.Row(
            controls=[
                ft.Stack(
                    alignment=ft.Alignment.BOTTOM_RIGHT,
                    margin=ft.Margin.only(left=10, right=3, top=3),
                    expand=100,
                    controls=[
                        ft.Image(
                            margin=ft.Margin.only(left=30, right=3, top=3),
                            expand=True,
                            border_radius=15,
                            src=thumbnail,
                        ),
                        ft.Container(
                            border_radius=10,
                            margin=ft.Margin.only(right=12, bottom=8),
                            bgcolor=colors["card"],
                            padding=ft.Padding.only(left=5, right=5, top=3, bottom=3),
                            content=ft.Text(
                                duration_str,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ],
                ),
                ft.Stack(
                    expand=50,
                    alignment=ft.Alignment.TOP_RIGHT,
                    controls=[
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            controls=[
                                ft.Text(
                                    title,
                                    margin=ft.Margin.only(right=5),
                                    color=colors["text"],
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    author,
                                    margin=ft.Margin.only(top=5),
                                    color=colors["text_secondary"],
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),
    )

    delete_btn = ft.IconButton(
        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
        margin=ft.Margin.only(right=15, top=10),
        on_click=lambda e, k=key, c=card: on_delete(k, c),
    )
    card.content.controls[1].controls.append(delete_btn)

    return card