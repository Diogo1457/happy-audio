import librosa
import soundfile as sf
import os
from rich.progress import Progress, SpinnerColumn, TextColumn
from music_accelerator.exceptions.audio_processing import (
    InvalidAudioInputError,
    AudioTimeStretchError,
    AudioPitchShiftError,
    AudioSaveError,
)

def accelerate_music(input_path, output_path=None, speed=1.25, pitch_shift=2, silent: bool = False):
    """
    Makes a song sound faster and happier (tempo + pitch increase).

    :param input_path: Path to the input audio file.
    :param output_path: Optional path to save the processed audio file.
    :param speed: Speed multiplier (default: 1.25).
    :param pitch_shift: Pitch shift in semitones (default: 2).
    :param silent: If True, suppresses the progress bar and console output.
    :raises InvalidAudioInputError: If the audio file is missing or cannot be loaded.
    :raises AudioTimeStretchError: If time stretching fails.
    :raises AudioPitchShiftError: If pitch shifting fails.
    :raises AudioSaveError: If saving the processed file fails.
    """
    if not os.path.isfile(input_path):
        raise InvalidAudioInputError(f"Input audio file not found: {input_path}")

    # Determine output file
    output_path = output_path or input_path.replace(".mp3", "_happy.mp3").replace(".wav", "_happy.wav")

    # Define progress steps
    steps = [
        "Loading audio",
        "Applying time stretch",
        "Applying pitch shift",
        "Saving output",
    ]

    def process_audio():
        """Inner function for main audio processing logic."""
        # Step 1: Load audio
        try:
            y, sr = librosa.load(input_path, sr=None)
        except Exception as e:
            raise InvalidAudioInputError(f"Error loading audio file '{input_path}': {e}")

        # Step 2: Apply speed-up
        try:
            y_fast = librosa.effects.time_stretch(y=y, rate=speed)
        except Exception as e:
            raise AudioTimeStretchError(f"Error applying time stretch: {e}")

        # Step 3: Apply pitch shift
        try:
            y_happy = librosa.effects.pitch_shift(y=y_fast, sr=sr, n_steps=pitch_shift)
        except Exception as e:
            raise AudioPitchShiftError(f"Error applying pitch shift: {e}")

        # Step 4: Save processed file
        try:
            sf.write(output_path, y_happy, sr)
        except Exception as e:
            raise AudioSaveError(f"Error saving output file '{output_path}': {e}")

        return output_path

    # === Silent Mode ===
    if silent:
        return process_audio()

    # === Verbose Mode with Progress Bar ===
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
    ) as progress:
        task = progress.add_task(steps[0], total=None)

        try:
            # Step 1
            progress.update(task, description=steps[0])
            y, sr = librosa.load(input_path, sr=None)

            # Step 2
            progress.update(task, description=steps[1])
            y_fast = librosa.effects.time_stretch(y=y, rate=speed)

            # Step 3
            progress.update(task, description=steps[2])
            y_happy = librosa.effects.pitch_shift(y=y_fast, sr=sr, n_steps=pitch_shift)

            # Step 4
            progress.update(task, description=steps[3])
            sf.write(output_path, y_happy, sr)

        except Exception as e:
            # Map exceptions to the correct type
            msg = str(e)
            if "load" in msg or "read" in msg:
                raise InvalidAudioInputError(msg)
            elif "stretch" in msg:
                raise AudioTimeStretchError(msg)
            elif "pitch" in msg:
                raise AudioPitchShiftError(msg)
            elif "save" in msg or "write" in msg:
                raise AudioSaveError(msg)
            else:
                raise
        finally:
            progress.update(task, description="[green]✅ Done!")

    return output_path
