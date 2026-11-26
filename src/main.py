import sys
import os

# Добавляем папку, где находится main.py, в пути поиска Python
if getattr(sys, 'frozen', False):
    # Если мы в скомпилированном .exe
    sys.path.insert(0, os.path.dirname(sys.executable))
else:
    # Если запускаем как обычный скрипт
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from app import App

def main(page: ft.Page):
    App(page)

if __name__ == "__main__":
    ft.run(main)