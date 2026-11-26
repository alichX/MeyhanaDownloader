import flet as ft
from flet_notifications import Notifications


# Запрашиваем разрешение (на Windows вернёт True сразу)
def system_notification():
    if Notifications().request_permissions():
        Notifications().show(
            id=1,
            title="MeyhanaConverter",
            body="Видео успешно скачано!"
        )