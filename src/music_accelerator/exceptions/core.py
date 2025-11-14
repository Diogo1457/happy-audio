from music_accelerator.exceptions import MusicAcceleratorError

class InvalidInputError(MusicAcceleratorError):
    """
    Raised when neither a valid URL nor file path is provided.
    """
    pass

class OutputPermissionError(MusicAcceleratorError):
    """
    Raised when the output directory is not writable.
    """
    pass

class FileTypeError(MusicAcceleratorError):
    """
    Raised when a provided file does not match the expected type.
    """
    pass
