from music_accelerator.exceptions import MusicAcceleratorError

class YouTubeDownloadError(MusicAcceleratorError):
    """
    Raised when downloading from YouTube fails.
    """
    pass

class YouTubeInvalidURLError(MusicAcceleratorError):
	"""
	Raised when the provided YouTube URL is invalid.
	"""
	pass