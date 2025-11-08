import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from utils.audio_processing import accelerate_music
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

class MoviePyProgressLogger:
    """Custom logger for MoviePy to update Rich progress bar."""

    def __init__(self, progress, task):
        self.progress = progress
        self.task = task

    def callback(self, **changes):
        """Called by MoviePy during write_videofile."""
        # MoviePy provides 'progress' as float 0-1
        progress = changes.get("progress")
        if progress is not None:
            self.progress.update(self.task, completed=progress * 100)

def video_accelerate_music(input_video: str, output_video: str, speed: float = 1.25, pitch_shift: float = 2):
    if not os.path.isfile(input_video):
        raise ValueError(f"Input video not found: {input_video}")

    valid_extensions = (".mp4", ".mkv", ".avi", ".mov", ".webm")
    ext = os.path.splitext(output_video)[1].lower()
    if ext not in valid_extensions:
        raise ValueError(f"Output file must be a video with extension {valid_extensions}")

    temp_audio_path = None
    temp_processed_audio = None
    video_clip = None
    new_audio = None

    try:
        # Load video
        video_clip = VideoFileClip(input_video)

        # Speed up video
        video_clip = video_clip.fx(vfx.speedx, factor=speed)

        # Extract audio to temporary WAV file
        temp_audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        video_clip.audio.write_audiofile(temp_audio_path, fps=44100, logger=None)

        # Process audio (speed + pitch)
        temp_processed_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        accelerate_music(temp_audio_path, temp_processed_audio, speed=speed, pitch_shift=pitch_shift)

        # Replace audio in video
        new_audio = AudioFileClip(temp_processed_audio)
        video_clip = video_clip.set_audio(new_audio)

        # Rich progress bar for video export
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Processing video...", total=100)

            video_clip.write_videofile(
                output_video,
                codec="libx264",
                audio_codec="aac",
                fps=video_clip.fps,
                logger=MoviePyProgressLogger(progress, task).callback(),
                verbose=False
            )

    finally:
        # Cleanup temp files
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if temp_processed_audio and os.path.exists(temp_processed_audio):
            os.remove(temp_processed_audio)

        # Close clips
        if video_clip:
            video_clip.close()
        if new_audio:
            new_audio.close()
