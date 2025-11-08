import librosa
import soundfile as sf
import os
from rich.progress import Progress, SpinnerColumn, TextColumn

def accelerate_music(input_path, output_path=None, speed=1.25, pitch_shift=2):
    """
    Makes a song sound faster and happier (tempo + pitch increase) with a progress bar.
    """
    if not os.path.isfile(input_path):
        raise ValueError(f"Input file not found: {input_path}")

    output_path = output_path or input_path.replace(".mp3", "_happy.mp3").replace(".wav", "_happy.wav")

    steps = ["Loading audio", "Applying time stretch", "Applying pitch shift", "Saving output"]

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
    ) as progress:
        task = progress.add_task(steps[0], total=None)

        # Step 1: Load audio
        try:
            y, sr = librosa.load(input_path, sr=None)
        except Exception as e:
            raise ValueError(f"Error loading audio file '{input_path}': {e}")

        progress.update(task, description=steps[1])

        # Step 2: Speed up
        try:
            y_fast = librosa.effects.time_stretch(y=y, rate=speed)
        except Exception as e:
            raise ValueError(f"Error applying time stretch: {e}")

        progress.update(task, description=steps[2])

        # Step 3: Pitch shift
        try:
            y_happy = librosa.effects.pitch_shift(y=y_fast, sr=sr, n_steps=pitch_shift)
        except Exception as e:
            raise ValueError(f"Error applying pitch shift: {e}")

        progress.update(task, description=steps[3])

        # Step 4: Save
        try:
            sf.write(output_path, y_happy, sr)
        except Exception as e:
            raise ValueError(f"Error saving output file '{output_path}': {e}")

        progress.update(task, description="[green]✅ Done!")

    return output_path
