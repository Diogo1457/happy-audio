from music_accelerator.exceptions import MusicAcceleratorError

class AudioProcessingError(MusicAcceleratorError):
    """
    Raised when there is an error during audio processing.
    """
    pass

class AudioAcceleratorError(Exception):
    """Base exception for all audio acceleration errors."""
    pass


class InvalidAudioInputError(AudioAcceleratorError):
    """Raised when the input audio file is missing or cannot be loaded."""
    pass


class AudioTimeStretchError(AudioAcceleratorError):
    """Raised when applying time stretch fails."""
    pass


class AudioPitchShiftError(AudioAcceleratorError):
    """Raised when applying pitch shift fails."""
    pass


class AudioSaveError(AudioAcceleratorError):
    """Raised when saving the processed audio file fails."""
    pass
