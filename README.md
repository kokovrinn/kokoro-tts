# Kokoro TTS

A modern desktop text-to-speech application built with **Kokoro v0.9.4** — an 82M-parameter neural TTS model.

## Features

- Session management with search and auto-save
- Text import from PDF, DOCX, TXT, MD, RST (drag & drop too)
- 3‑part voice selection: Language → Tone → Voice
- Speed control, output format (.wav, .mp3, .flac, .aiff)
- Auto‑save audio to configurable output folder
- Built-in audio player with volume control
- Dark / Light theme
- Cross-platform (macOS, Linux, Windows)

## Requirements

- Python 3.10+
- FFmpeg (for QMediaPlayer audio playback)

## Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows (cmd)
venv\Scripts\Activate.ps1       # Windows (PowerShell)

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python app/main.py

# Reset everything
python app/main.py --reset

# Reset only config or model cache
python app/main.py --reset-config
python app/main.py --reset-model

# Force download dialog on next launch
python app/main.py --show-download
```

## Build (macOS)

```bash
pip install pyinstaller
pyinstaller build.spec
```

The `.app` bundle will be created in the `dist/` directory.

*Note: The build spec uses macOS-specific paths for espeak-ng. Contributions for Linux/Windows build configs are welcome.*

## License

MIT — see [LICENSE](LICENSE).

## Credits

- [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) TTS model by **hexgrad**
- Built with PySide6, PyMuPDF, soundfile, Transformers
