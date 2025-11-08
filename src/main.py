import argparse
from rich.console import Console
from rich.panel import Panel
from music_accelerator.core import music_accelarator

console = Console()

def main():
    parser = argparse.ArgumentParser(
        description="[magenta]🎵 Accelerate music or videos (speed up + pitch shift)[/magenta]"
    )

    # Mutually exclusive input: local file or YouTube
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to local audio or video file")
    group.add_argument("-y", "--youtube", help="YouTube URL (audio or video)")

    # Options
    parser.add_argument("-v", "--video", action="store_true",
                        help="Process as video instead of audio (applies to local file or YouTube)")
    parser.add_argument("--no-cache", action="store_true",
                        help="Do not use cache when downloading YouTube content")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("-s", "--speed", type=float, default=1.25,
                        help="Speed multiplier (default 1.25)")
    parser.add_argument("-p", "--pitch-shift", type=float, default=2,
                        help="Pitch shift in semitones (default +2)")

    args = parser.parse_args()

    console.print(Panel.fit(f"""
⚙️  Configuration:
    Speed: {args.speed}x
    Pitch shift: +{args.pitch_shift} semitones
    Video mode: {'Yes' if args.video else 'No'}
    Use cache: {'No' if args.no_cache else 'Yes'}
    """, title="🎛️ Settings", border_style="cyan"))

    try:
        music_accelarator(
            url=args.youtube,
            file_path=args.file,
            output=args.output,
            speed=args.speed,
            pitch_shift=args.pitch_shift,
            video=args.video,
            use_cache=not args.no_cache
        )
    except Exception as e:
        console.print(f"[red]❌ Failed:[/red] {e}")

if __name__ == "__main__":
    main()
