from rich.console import Console
from utils.youtube import download_youtube_audio
from utils.audio_processing import accelerate_music
from music_accelerator.constants.constants import AUDIO_OUTPUT_DEFAULT
import os
import sys

console = Console()

def output_file_determination(output_path: str) -> str:
    """
    Determine and validate output file path.
    """
    output_file = output_path or AUDIO_OUTPUT_DEFAULT
    directory = os.path.dirname(os.path.abspath(output_file)) or "."
    if not os.access(directory, os.W_OK):
        console.print(f"❌[red] Cannot write to output directory:[/red] {directory}")
        sys.exit(1)
    return output_file


def music_accelarator(url: str = None, audio_path: str = None, output: str = None,
               speed: float = 1.25, pitch_shift: float = 2):
    """
    Accelerate and pitch-shift a song.
    Can process either a local audio file or a YouTube URL.

    :param url: YouTube URL (audio only)
    :param audio_path: Local audio file path
    :param output: Output file path (optional)
    :param speed: Speed multiplier (default 1.25)
    :param pitch_shift: Pitch shift in semitones (default 2)
    """
    if not url and not audio_path:
        raise ValueError("You must provide either a YouTube URL or a local audio_path.")

    # Determine output file
    output_file = output_file_determination(output)

    # Determine input file
    if url:
        try:
            input_file = download_youtube_audio(url)
            delete_original = True
        except Exception as e:
            console.print(f"[red]❌ Error downloading YouTube audio:[/red] {e}")
            raise
    else:
        input_file = audio_path
        delete_original = False

    console.print(f"[cyan]🎵 Processing audio:[/cyan] {input_file}")

    try:
        accelerate_music(input_file, output_file, speed, pitch_shift)
        if delete_original:
            os.remove(input_file)
    except Exception as e:
        console.print(f"[red]❌ Error processing audio:[/red] {e}")
        raise

    console.print(f"[bold green]🎉 All done![/bold green] Audio saved to [bold cyan]{output_file}[/bold cyan]!")

    return output_file
