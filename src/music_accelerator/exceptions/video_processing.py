from music_accelerator.exceptions import MusicAcceleratorError

class VideoProcessingError(MusicAcceleratorError):
    """
    Raised when there is an error during video processing.
    """
    pass

class VideoAcceleratorError(Exception):
    """Base exception for all video acceleration errors."""
    pass


class InvalidVideoInputError(VideoAcceleratorError):
    """Raised when the input video file is missing or invalid."""
    pass


class InvalidVideoOutputError(VideoAcceleratorError):
    """Raised when the output video file has an unsupported extension."""
    pass


class VideoAudioExtractionError(VideoAcceleratorError):
    """Raised when audio extraction from video fails."""
    pass


class VideoAudioProcessingError(VideoAcceleratorError):
    """Raised when processing or reattaching the audio fails."""
    pass


class VideoExportError(VideoAcceleratorError):
    """Raised when exporting the final accelerated video fails."""
    pass
