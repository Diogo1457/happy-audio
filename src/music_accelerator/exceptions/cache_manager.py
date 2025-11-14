class CacheError(Exception):
    """Base exception for all cache-related errors."""
    pass


class InvalidYouTubeURLError(CacheError):
    """Raised when the provided YouTube URL is invalid."""
    pass


class CacheFileError(CacheError):
    """Raised when the cache file cannot be read or written."""
    pass


class CacheFileRemovalError(CacheError):
    """Raised when a cached file cannot be deleted."""
    pass
