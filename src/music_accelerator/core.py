from rich.console import Console
from utils.youtube import download_youtube_audio
from utils.audio_processing import accelerate_music
from utils.video_processing import video_accelerate_music
from music_accelerator.constants.constants import AUDIO_OUTPUT_DEFAULT, VIDEO_OUTPUT_DEFAULT
import os
import sys

console = Console()

def output_file_determination(output_path: str, video: bool) -> str:
    """
    Determine and validate output file path.
    """
    output_file = output_path or (AUDIO_OUTPUT_DEFAULT if not video else VIDEO_OUTPUT_DEFAULT)
    directory = os.path.dirname(os.path.abspath(output_file)) or "."
    if not os.access(directory, os.W_OK):
        console.print(f"❌[red] Cannot write to output directory:[/red] {directory}")
        sys.exit(1)
    return output_file


def music_accelarator(url: str = None,
                      file_path: str = None,
                      output: str = None,
                      speed: float = 1.25,
                      pitch_shift: float = 2,
                      video: bool = False,
                      use_cache: bool = True):
    """
    Accelerate and pitch-shift a song or video.
    Can process either a local file or a YouTube URL.

    :param url: YouTube URL
    :param file_path: Local file path
    :param output: Output file path (optional)
    :param speed: Speed multiplier (default 1.25)
    :param pitch_shift: Pitch shift in semitones (default 2)
    :param video: If True, process as video (replace audio in video)
    :param use_cache: If True, use YouTube cache when downloading
    """
    if not url and not file_path:
        raise ValueError("You must provide either a YouTube URL or a local file_path.")

    # Determine output file
    output_file = output_file_determination(output, video)

    if url:
        try:
            input_file = download_youtube_audio(url, video=video, use_cache=use_cache)
        except Exception as e:
            console.print(f"[red]❌ Error downloading YouTube content:[/red] {e}")
            raise
    else:
        input_file = file_path

    console.print(f"[cyan]🎵 Processing 'audio' from :[/cyan] {input_file}")

    try:
        if video:
            console.print(f"[cyan]🎬 Processing video:[/cyan] {input_file}")
            video_accelerate_music(input_file, output_file, speed, pitch_shift)
            console.print(f"[bold green]🎉 Video done![/bold green] Saved to: [bold cyan]{output_file}[/bold cyan]")
        else:
            accelerate_music(input_file, output_file, speed, pitch_shift)
    except Exception as e:
        console.print(f"[red]❌ Error processing {'video' if video else 'audio'}:[/red] {e}")
        raise

    console.print(f"[bold green]🎉 All done![/bold green] Output saved to [bold cyan]{output_file}[/bold cyan]!")

    return output_file
