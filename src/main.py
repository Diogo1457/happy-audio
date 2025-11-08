from rich.console import Console
from rich.panel import Panel
import argparse
import sys
import os
from constants.constants import AUDIO_OUTPUT_DEFAULT
from utils.youtube import download_youtube_audio
from utils.audio import accelerate_music

console = Console()

def output_file_determination(output_path: str) -> str:
    """
    Determine and validate output file path.
    :param output_path: User-specified output path
    :return: Validated output file path
    """
    output_file = output_path or AUDIO_OUTPUT_DEFAULT
    directory = os.path.dirname(os.path.abspath(output_file)) or "."
    if not os.access(directory, os.W_OK):
        console.print(f"❌[red] Cannot write to output directory:[/red] {directory}")
        sys.exit(1)
    return output_file

def main():
    parser = argparse.ArgumentParser(description="[magenta]🎵 Accelerate music or videos (speed up + pitch shift)[/magenta]")

    # Input (mutually exclusive)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--audio", help="Path to local audio file")
    group.add_argument("-y", "--youtube", help="YouTube URL (audio only)")

    # Options
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("-s", "--speed", type=float, default=1.25, help="Speed multiplier (default 1.25)")
    parser.add_argument("-ps", "--pitch-shift", type=float, default=2, help="Pitch shift in semitones (default +2)")

    args = parser.parse_args()

    # Summary panel
    console.print(Panel.fit(f"""
⚙️  Configuration:
    Speed: {args.speed}x
    Pitch shift: +{args.pitch_shift} semitones
    """, title="🎛️ Settings", border_style="cyan"))

    # Determine output file
    output_file = output_file_determination(args.output)

    # Determine input file
    if args.youtube:
        try:
            input_file = download_youtube_audio(args.youtube)
        except Exception as e:
            console.print(f"[red]❌ Error downloading YouTube audio:[/red] {e}")
            sys.exit(1)
    elif args.audio:
        input_file = args.audio

    console.print(f"[cyan]🎵 Processing audio:[/cyan] {input_file}")
    
    try:
        accelerate_music(input_file, output_file, args.speed, args.pitch_shift)
        if args.youtube:
            os.remove(input_file)  # Clean up downloaded file
    except Exception as e:
        console.print(f"[red]❌ Error processing audio:[/red] {e}")
        sys.exit(1)

    console.print(f"[bold green]🎉 All done![/bold green] Audio saved to [bold cyan]{output_file}[/bold cyan]!")

if __name__ == "__main__":
    main()
