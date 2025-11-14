from music_accelerator.constants.constants import AUDIO_OUTPUT_DEFAULT, VIDEO_OUTPUT_DEFAULT
from music_accelerator.exceptions.core import OutputPermissionError, FileTypeError
import mimetypes
import os

def output_file_determination(output_path: str, video: bool) -> str:
    """
    Determine and validate output file path.
    """
    output_file = output_path or (AUDIO_OUTPUT_DEFAULT if not video else VIDEO_OUTPUT_DEFAULT)
    directory = os.path.dirname(os.path.abspath(output_file)) or "."
    if not os.access(directory, os.W_OK):
        raise OutputPermissionError(f"Cannot write to output directory: {directory}")
    return output_file


def check_file_type(file_path: str, expected_types: list[str], description: str):
    """
    Validate the file type.

    :param file_path: Path to file
    :param expected_types: List of acceptable MIME types
    :param description: Description for error messages
    :raises FileTypeError: If file type does not match expected
    """
    if not file_path:
        return
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not any(mime_type.startswith(t) for t in expected_types):
        raise FileTypeError(f"[red]❌ Invalid {description} file type:[/red] {file_path}")
