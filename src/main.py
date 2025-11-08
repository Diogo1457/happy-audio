import argparse
from rich.console import Console
from rich.panel import Panel
from music_accelerator.core import music_accelarator

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="[magenta]🎵 Accelerate music or videos (speed up + pitch shift)[/magenta]"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--audio", help="Path to local audio file")
    group.add_argument("-y", "--youtube", help="YouTube URL (audio only)")

    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("-s", "--speed", type=float, default=1.25, help="Speed multiplier (default 1.25)")
    parser.add_argument("-ps", "--pitch-shift", type=float, default=2, help="Pitch shift in semitones (default +2)")

    args = parser.parse_args()

    console.print(Panel.fit(f"""
⚙️  Configuration:
    Speed: {args.speed}x
    Pitch shift: +{args.pitch_shift} semitones
    """, title="🎛️ Settings", border_style="cyan"))

    try:
        music_accelarator(
            url=args.youtube,
            audio_path=args.audio,
            output=args.output,
            speed=args.speed,
            pitch_shift=args.pitch_shift
        )
    except Exception as e:
        console.print(f"[red]❌ Failed:[/red] {e}")

if __name__ == "__main__":
    main()
