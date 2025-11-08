import yt_dlp
import os

def download_youtube_audio(url: str) -> str:
    """
    Download YouTube audio only (quiet, non-verbose) and convert to MP3.

    :param url: YouTube URL
    :return: Path to downloaded audio file (MP3)
    :raises ValueError: if URL is not a valid YouTube link
    """

    out_template = "youtube_audio.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "noplaylist": True,
        "quiet": True,         # No console output
        "no_warnings": True,   # Suppress warnings
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

            # Convert extension to mp3
            base, _ = os.path.splitext(filename)
            filename = base + ".mp3"

    except Exception as e:
        raise RuntimeError(f"Failed to download audio: {e}")

    return filename