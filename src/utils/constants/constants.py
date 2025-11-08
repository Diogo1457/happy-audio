import os
import re

HOME_DIR = os.path.expanduser("~")

CONFIG_DIR = os.path.join(HOME_DIR, ".cache", "happy-audio")
CACHE_DIR = os.path.join(CONFIG_DIR, "files")
CACHE_FILE = os.path.join(CONFIG_DIR, "config.json")
YOUTUBE_REGEX = re.compile(r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[0-9A-Za-z_-]{11}(&.*)?$')

YOUTUBE_ID_REGEX = re.compile(
    r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)"
)