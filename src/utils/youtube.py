import os
import yt_dlp
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, DownloadColumn, TransferSpeedColumn
from utils.cache_manager import CacheManager
from utils.constants.constants import CACHE_DIR, YOUTUBE_REGEX

console = Console()
cache_manager = CacheManager()

def download_youtube_audio(url: str, video: bool = False, use_cache: bool = True) -> str:
    """
    Download YouTube audio or video, using cache and progress bar.

    :param url: YouTube URL
    :param video: If True, download full video; otherwise audio only
    :param use_cache: If True, reuse cached file if exists
    :return: Path to downloaded file
    :raises ValueError: if URL is invalid
    """
    if not YOUTUBE_REGEX.match(url):
        raise ValueError("Invalid YouTube URL")

    # Extract video ID
    video_id = CacheManager.extract_video_id(url)

    # Check cache
    cached_path = cache_manager.get(video_id, video=video)
    if cached_path and use_cache:
        console.print(f"[yellow]⚡ Using cached {'video' if video else 'audio'}:[/yellow] {cached_path}")
        return cached_path

    # If audio requested, fallback to mp4 if mp3 not available
    if not video:
        mp4_path = os.path.join(CACHE_DIR, f"{video_id}.mp4")
        if use_cache and os.path.exists(mp4_path):
            console.print(f"[yellow]⚡ Using cached video as audio source:[/yellow] {mp4_path}")
            return mp4_path

    # Prepare output filename
    ext = ".mp4" if video else ".mp3"
    output_path = os.path.join(CACHE_DIR, f"{video_id}{ext}")

    # yt-dlp options
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "no_warnings": True,
        "outtmpl": os.path.join(CACHE_DIR, video_id),
        "progress_hooks": [],
    }

    if not video:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        ydl_opts["format"] = "bestvideo+bestaudio/best"
        ydl_opts["merge_output_format"] = "mp4"

    # Progress bar
    progress = Progress(
        TextColumn("[bold blue]{task.fields[title]}[/bold blue]"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True
    )

    with progress:
        task = progress.add_task("Downloading...", total=None, title="🎵 YouTube Download")

        # Hook to update progress
        def hook(d):
            if d['status'] == 'downloading':
                progress.update(task, completed=d.get('downloaded_bytes', 0), total=d.get('total_bytes', 0))
            elif d['status'] == 'finished':
                progress.console.print("[green]✅ Download complete, finalizing...[/green]")

        ydl_opts["progress_hooks"].append(hook)

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Unknown Title")
            duration = round(info.get("duration", 0) / 60, 2)
            uploader = info.get("uploader", "Unknown")

            console.print(f"\n🎥 [bold cyan]Title:[/bold cyan] {title}")
            console.print(f"📺 [bold cyan]Uploader:[/bold cyan] {uploader}")
            console.print(f"⏱️ [bold cyan]Duration:[/bold cyan] {duration} minutes\n")

    # Save to cache
    cache_manager.add(video_id, video)
    console.print(f"[green]✅ File saved to:[/green] {output_path}")

    return output_path
