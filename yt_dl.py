import os
import yt_dlp
import uuid

queue = []
def yt_dl(URL):
    filename = f'{uuid.uuid4()}.m4a'
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': filename,
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            

        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URL)

    return filename

def delete_song(file):
    if os.path.exists(file):
        os.remove(file)

