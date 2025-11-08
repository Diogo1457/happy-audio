# 🎵 Music Accelerator CLI/GUI

**Make your music faster and happier with a simple command-line tool!**

---

## 📝 Overview

**Audio Accelerator** is a Python CLI tool that allows you to:

* Speed up audio tracks (tempo)
* Increase pitch to make the music feel brighter/happier
* Download audio directly from YouTube for processing

> ⚠️ Video support and GUI are planned but not yet implemented.

---

## 🚀 Features

* Increase **speed** (tempo) of an audio track
* Increase **pitch** (in semitones)
* Quiet (non-verbose) YouTube audio downloads
* Validates input/output paths
* Automatically deletes temporary YouTube audio files after processing

---

## 🧩 Dependencies

### Python packages

These are already included in `requirements.txt`:

```bash
pip install librosa soundfile yt-dlp rich
```

## System dependencies

### FFmpeg (required for audio extraction and conversion)

### Installation examples:

#### Ubuntu/Debian:
```bash
sudo apt install ffmpeg
```

#### macOS (Homebrew):
```bash
brew install ffmpeg
```

#### Windows:
- Download from [FFmpeg.org](https://ffmpeg.org/)
- Add ffmpeg to your system PATH

## 💻 Installation
1. Clone the repository:
```bash
git clone https://github.com/Diogo1457/happy-audio.git
cd happy-audio
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙️ Usage

### 🎵 Process a local audio file
```bash
python main.py -a path/to/song.mp3 -s 1.25 -ps 2 -o output.mp3
```

### 🔊 Download and process YouTube audio
```bash
python main.py -y https://www.youtube.com/watch?v=hT_nvWreIhg -s 1.3 -ps 3
```

| Flag | Description | Default |
|------|-------------|---------|
| `-a`, `--audio` | Path to a local audio file | — |
| `-y`, `--youtube` | YouTube URL (audio only) | — |
| `-o`, `--output` | Output file path | `output.mp3` |
| `-s`, `--speed` | Speed multiplier | `1.25` |
| `-ps`, `--pitch-shift` | Pitch shift in semitones | `+2` |

## 😎 TODO

- [x] Audio acceleration
- [ ] Video acceleration
- [ ] GUI (desktop interface)



## 🗒️ Notes
- Works with .mp3, .wav, .ogg, .flac, etc.

- Requires ffmpeg to be installed and accessible in PATH.

- Designed for simplicity and clean terminal output using Rich.

- Tested on Windows, macOS, and Linux.