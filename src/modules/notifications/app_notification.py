import flet as ft
import flet_shadcn_ui as shad

def app_notification(page: ft.Page):

    page.show_dialog(
        shad.Toast(
            title="Готово!",
            description="Видео успешно скачано.",
            variant=shad.ToastVariant.PRIMARY,
            duration=5000,
        )
    )
