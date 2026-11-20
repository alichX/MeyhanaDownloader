import yt_dlp
import os

infoList = {}

def config(format=None, ui_callback=None):
    ydl_opts = {
        'ffmpeg_location': r'C:\ffmpeg\bin',
        'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'quiet': False,
        'verbose': True,
    }

    if format == "MP3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata', 'add_metadata': True},
                {'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'},
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
            ]
        })
        pass
    elif format == "MP4":
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'postprocessors': [
                {'key': 'FFmpegThumbnailsConvertor','format': 'jpg'},
                {'key': 'EmbedThumbnail','already_have_thumbnail': False},
                {'key': 'FFmpegMetadata', 'add_metadata': True},
            ]
        })

    # В ПРОЦЕССЕ РАЗРАБОТКИ...
    if ui_callback:
        def progress_hook(d):
            if d['status'] == 'downloading':
                # Вычисляем проценты (иногда total_bytes нет, поэтому используем estimate)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)

                if total > 0:
                    percent = downloaded / total

                    # Вызываем функцию из main.py
                    ui_callback(percent, "Скачивание")

            elif d['status'] == 'finished':
                # Скачивание закончено, но началась работа FFmpeg (конвертация/вшивание)
                ui_callback(1.0, "", "Обработка FFmpeg...")

        ydl_opts['progress_hooks'] = [progress_hook]
    return ydl_opts

async def get_video_info(urls: list, format):
    for url in urls:
        try:
            with yt_dlp.YoutubeDL(config(format)) as ydl:
                info_result = ydl.extract_info(url, download=False)

                infoList[str(url)] = [info_result.get('title'), info_result.get('thumbnail'), info_result.get('uploader'), info_result.get('duration')]
        except Exception as e:
            print(f"Ошибка при получении инфо: {e}")
            pass
    print(infoList)

    return infoList


def download_video(format):
    for url in list(infoList.keys()):
        try:
            with yt_dlp.YoutubeDL(config(format)) as ydl:
                ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
            return
    infoList.clear()




