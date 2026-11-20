import base64
from io import BytesIO
from pathlib import Path
from usb_manager import find_usb_drivers
from mutagen.id3 import ID3
from mutagen import File
from PIL import Image
import flet as ft

def get_mp3_cover_base64(file_path: str | Path, size: int = 64) -> str | None:
    try:
        for audio in file_path.iterdir():




            for key in audio.tags.keys():
                if key.startswith("APIC"):
                    image_data = audio.tags[key].data
                    break
            else:
                return None  # обложки нет


            img = Image.open(BytesIO(image_data))
            img.thumbnail((size, size))


            buffer = BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")


    except Exception:
        return None

print(get_mp3_cover_base64(find_usb_drivers()))
