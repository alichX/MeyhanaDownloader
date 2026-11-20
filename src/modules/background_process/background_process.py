import flet as ft

def main(page: ft.Page):
    # Создаем список с элементами
    my_list = ft.ListView(
        expand=True,
        spacing=10,

        controls=[
            ft.ListTile(title=ft.Text(f"Элемент списка {i}")) for i in range(30)
        ],
    )

    # Оборачиваем ListView в ShaderMask
    faded_list = ft.ShaderMask(
        content=my_list,
        blend_mode=ft.BlendMode.DST_IN, # 👈 Режим наложения для эффекта прозрачности
        shader=ft.LinearGradient(
            begin=ft.alignment.T,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.TRANSPARENT, # Верхний край полностью прозрачный
                ft.Colors.BLACK,       # Верхняя часть списка непрозрачная
                ft.Colors.BLACK,       # Нижняя часть списка непрозрачная
                ft.Colors.TRANSPARENT, # Нижний край полностью прозрачный
            ],
            stops=[0.0, 0.15, 0.85, 1.0], # 👈 Управляем зоной затухания (15% сверху и снизу)
        ),
        expand=True,
    )

    page.add(faded_list)

ft.run(main)