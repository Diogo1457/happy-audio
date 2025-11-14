import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from utils.audio_processing import accelerate_music
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from music_accelerator.exceptions.video_processing import (
    InvalidVideoInputError,
    InvalidVideoOutputError,
    VideoAudioExtractionError,
    VideoAudioProcessingError,
    VideoExportError,
)

console = Console()

class MoviePyProgressLogger:
    """Custom logger for MoviePy to update Rich progress bar."""

    def __init__(self, progress, task):
        self.progress = progress
        self.task = task

    def callback(self, **changes):
        """Called by MoviePy during write_videofile."""
        progress = changes.get("progress")
        if progress is not None:
            self.progress.update(self.task, completed=progress * 100)


def video_accelerate_music(input_video: str, output_video: str, speed: float = 1.25, pitch_shift: float = 2, silent: bool = False):
    """
    Accelerate a video and pitch-shift its audio track.

    :param input_video: Path to the input video file.
    :param output_video: Path to save the processed output video.
    :param speed: Playback speed multiplier (default 1.25).
    :param pitch_shift: Pitch shift in semitones (default 2).
    :param silent: If True, disables console output and progress bars.
    :raises InvalidVideoInputError: If input video file is missing.
    :raises InvalidVideoOutputError: If output file extension is invalid.
    :raises VideoAudioExtractionError: If audio extraction fails.
    :raises VideoAudioProcessingError: If audio processing fails.
    :raises VideoExportError: If video export fails.
    """
    if not os.path.isfile(input_video):
        raise InvalidVideoInputError(f"Input video not found: {input_video}")

    valid_extensions = (".mp4", ".mkv", ".avi", ".mov", ".webm")
    ext = os.path.splitext(output_video)[1].lower()
    if ext not in valid_extensions:
        raise InvalidVideoOutputError(f"Output file must have one of these extensions: {valid_extensions}")

    temp_audio_path = None
    temp_processed_audio = None
    video_clip = None
    new_audio = None

    try:
        try:
            video_clip = VideoFileClip(input_video, verbose=not silent)
        except Exception as e:
            raise InvalidVideoInputError(f"Failed to load video file: {e}")

        try:
            # Speed up the video
            video_clip = video_clip.fx(vfx.speedx, factor=speed)

            # Extract audio to temporary WAV
            temp_audio_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            video_clip.audio.write_audiofile(
                temp_audio_path, 
                fps=44100, 
                logger=None if silent else None  # MoviePy logs disabled if silent
            )
        except Exception as e:
            raise VideoAudioExtractionError(f"Error extracting audio from video: {e}")

        try:
            # Process the extracted audio (silent flag passed through)
            temp_processed_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            accelerate_music(temp_audio_path, temp_processed_audio, speed=speed, pitch_shift=pitch_shift, silent=silent)
        except Exception as e:
            raise VideoAudioProcessingError(f"Error processing video audio: {e}")

        try:
            # Replace processed audio in video
            new_audio = AudioFileClip(temp_processed_audio)
            video_clip = video_clip.set_audio(new_audio)

            if silent:
                # No progress bars, no logs
                video_clip.write_videofile(
                    output_video,
                    codec="libx264",
                    audio_codec="aac",
                    fps=video_clip.fps,
                    logger=None,
                    verbose=False,
                )
            else:
                # Export video with Rich progress bar
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
                        logger=MoviePyProgressLogger(progress, task).callback,
                        verbose=False
                    )

        except Exception as e:
            raise VideoExportError(f"Error exporting video: {e}")

    finally:
        # Cleanup temporary files
        for temp_path in (temp_audio_path, temp_processed_audio):
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

        # Close clips
        if video_clip:
            video_clip.close()
        if new_audio:
            new_audio.close()
