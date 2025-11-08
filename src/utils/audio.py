import librosa
import soundfile as sf
import os


def accelerate_music(input_path, output_path=None, speed=1.25, pitch_shift=2):
    """
    Makes a song sound faster and happier (tempo + pitch increase).

    :param input_path: Path to input audio file
    :param output_path: Path to save processed audio (optional)
    :param speed: How much faster to make it (e.g., 1.25 = 25% faster)
    :param pitch_shift: Pitch increase in semitones (e.g., 2 = a bit higher/brighter)
    :raises ValueError: on any failure (file not found, processing error, or save error)
    :return: Path to saved output file
    """

    if not os.path.isfile(input_path):
        raise ValueError(f"Input file not found: {input_path}")

    try:
        # Load audio
        y, sr = librosa.load(input_path, sr=None)
    except Exception as e:
        raise ValueError(f"Error loading audio file '{input_path}': {e}")

    try:
        # Speed up (shorter duration)
        y_fast = librosa.effects.time_stretch(y=y, rate=speed)
    except Exception as e:
        raise ValueError(f"Error applying time stretch: {e}")

    try:
        # Raise pitch
        y_happy = librosa.effects.pitch_shift(y=y_fast, sr=sr, n_steps=pitch_shift)
    except Exception as e:
        raise ValueError(f"Error applying pitch shift: {e}")

    try:
        # Save to output
        sf.write(output_path, y_happy, sr)
    except Exception as e:
        raise ValueError(f"Error saving output file '{output_path}': {e}")

    # Return the path to the saved file
    return output_path
