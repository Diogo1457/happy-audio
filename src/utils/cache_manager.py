import os
import json
from collections import OrderedDict
from utils.constants.constants import CONFIG_DIR, CACHE_DIR, CACHE_FILE, YOUTUBE_ID_REGEX
from music_accelerator.exceptions.cache_manager import (
    CacheFileError,
    CacheFileRemovalError,
    InvalidYouTubeURLError
)

class CacheManager:
    """Manages cached YouTube downloads with a maximum of 2 entries using <video-id>-mp3/mp4."""

    MAX_ENTRIES = 2

    def __init__(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        os.makedirs(CACHE_DIR, exist_ok=True)
        if not os.path.exists(CACHE_FILE):
            self._write_cache({})

    def _load_cache(self):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f, object_pairs_hook=OrderedDict)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise CacheFileError(f"Failed to read cache file: {e}")

    def _write_cache(self, data):
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise CacheFileError(f"Failed to write cache file: {e}")

    @staticmethod
    def extract_video_id(url: str) -> str:
        match = YOUTUBE_ID_REGEX.search(url)
        if not match:
            raise InvalidYouTubeURLError(f"Invalid YouTube video URL: {url}")
        return match.group(1)

    def get(self, video_id: str, video: bool) -> str:
        """Return cached file path if exists and matches requested type."""
        ext = "mp4" if video else "mp3"
        key = f"{video_id}-{ext}"
        cache = self._load_cache()
        filename = cache.get(key)
        if filename:
            file_path = os.path.join(CACHE_DIR, filename)
            if os.path.exists(file_path):
                return file_path
        return None

    def add(self, video_id: str, video: bool):
        """Add a new cache entry. Keep max 2 entries; remove oldest if necessary."""
        ext = "mp4" if video else "mp3"
        filename = f"{video_id}.{ext}"
        filepath = os.path.join(CACHE_DIR, filename)
        key = f"{video_id}-{ext}"

        cache = self._load_cache()

        # Remove if exists to move to end
        if key in cache:
            cache.pop(key)

        cache[key] = filepath

        # Trim oldest entries if exceed MAX_ENTRIES
        while len(cache) > self.MAX_ENTRIES:
            oldest_key, oldest_file = cache.popitem(last=False)
            oldest_path = os.path.join(CACHE_DIR, oldest_file)
            if os.path.exists(oldest_path):
                try:
                    os.remove(oldest_path)
                except Exception as e:
                    raise CacheFileRemovalError(f"Failed to remove cached file {oldest_path}: {e}")

        self._write_cache(cache)
        self.clean_cache()

    def clean_cache(self):
        """Remove missing files from cache."""
        cache = self._load_cache()
        cleaned = OrderedDict()
        removed_count = 0

        for key, filename in cache.items():
            file_path = os.path.join(CACHE_DIR, filename)
            if os.path.exists(file_path):
                cleaned[key] = filename
            else:
                removed_count += 1

        self._write_cache(cleaned)
        return removed_count
