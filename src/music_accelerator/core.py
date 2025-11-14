from rich.console import Console
from utils.youtube import download_youtube_audio
from utils.audio_processing import accelerate_music
from utils.video_processing import video_accelerate_music
from music_accelerator.constants.constants import AUDIO_OUTPUT_DEFAULT, VIDEO_OUTPUT_DEFAULT
from utils.utils import output_file_determination, check_file_type
from music_accelerator.exceptions.audio_processing import AudioProcessingError
from music_accelerator.exceptions.video_processing import VideoProcessingError
from music_accelerator.exceptions.youtube import YouTubeDownloadError
from music_accelerator.exceptions.core import InvalidInputError, OutputPermissionError, FileTypeError

console = Console()

def music_accelarator(url: str = None,
                      file_path: str = None,
                      output: str = None,
                      speed: float = 1.25,
                      pitch_shift: float = 2,
                      video: bool = False,
                      use_cache: bool = True,
                      lyrics: str = None,
                      background: str = None,
                      silent: bool = False) -> str:
    """
    Accelerate and pitch-shift a song or video.
    Can process either a local file or a YouTube URL.

    :param lyrics: Optional lyrics file (txt)
    :param background: Optional background media (video/photo)
    """
    if not url and not file_path:
        raise InvalidInputError("You must provide either a YouTube URL or a local file_path.")

    # Check file types
    try:
        if lyrics:
            check_file_type(lyrics, ["text"], "lyrics")
        if background:
            check_file_type(background, ["image", "video"], "background")
        if file_path:
            if video:
                check_file_type(file_path, ["video"], "video")
            else:
                check_file_type(file_path, ["audio"], "audio")
    except FileTypeError as e:
        raise FileTypeError(e)

    # Lyrics/background logic
    if lyrics:
        if not file_path and not url:
            raise InvalidInputError("Cannot process lyrics without a file or YouTube URL.")
        if video:
            # For video mode, background not required
            console.print("[cyan]🎤 Lyrics will be merged with the video[/cyan]")
            join_lyrics_to_video(file_path or url, lyrics, output)
            return output or VIDEO_OUTPUT_DEFAULT
        else:
            # Audio mode requires background
            if not background:
                raise InvalidInputError("Audio mode with lyrics requires a background file.")
    
    # Determine output file
    try:
        output_file = output_file_determination(output, video)
    except OutputPermissionError as e:
        raise OutputPermissionError(f"[red]❌ {e}[/red]")

    if url:
        try:
            input_file = download_youtube_audio(url, video=video, use_cache=use_cache)
        except Exception as e:
            raise YouTubeDownloadError(f"[red]❌ Error downloading YouTube content:[/red] {e}")
    else:
        input_file = file_path

    if video:
        if not silent:
            console.print(f"[cyan]🎬 Processing video:[/cyan] {input_file}")
        try:
            video_accelerate_music(input_file, output_file, speed, pitch_shift, silent=silent)
        except Exception as e:
            raise VideoProcessingError(f"[red]❌ Error processing video:[/red] {e}")
        if not silent:
            console.print(f"[bold green]🎉 Video done![/bold green] Saved to: [bold cyan]{output_file}[/bold cyan]")
    else:
        if not silent:
            console.print(f"[cyan]🎵 Processing audio:[/cyan] {input_file}")
        try:
            accelerate_music(input_file, output_file, speed, pitch_shift)
        except Exception as e:
            raise AudioProcessingError(f"[red]❌ Error processing audio:[/red] {e}")

    if not silent:
        console.print(f"[bold green]🎉 All done![/bold green] Output saved to [bold cyan]{output_file}[/bold cyan]!")

    return output_file