# Contributing

Thanks for considering contributing to Kokoro TTS.

## Report a Bug

Open an [issue](https://github.com/kokovrinn/kokoro-tts/issues) and include:
- Your OS (macOS / Linux / Windows)
- What you did, what happened, and what you expected

## Suggest a Feature

Open an [issue](https://github.com/kokovrinn/kokoro-tts/issues) describing what you want and why.

## Submit Code

1. **Fork** the repo (click Fork on GitHub — creates a copy under your account)
2. **Clone** your fork: `git clone https://github.com/YOUR_USER/kokoro-tts.git`
3. **Create a branch**: `git checkout -b feature/your-feature`
4. Make your changes
5. Run `ruff check app/` and fix any errors
6. Test the app: `python app/main.py`
7. **Push** to your fork: `git push origin feature/your-feature`
8. Open a **Pull Request** on GitHub from your branch to `kokovrinn/kokoro-tts` `main`

Only the repo owner has write access. PRs are reviewed before merging.

## Development Setup

```bash
git clone https://github.com/YOUR_USER/kokoro-tts.git
cd kokoro-tts
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install ruff
python app/main.py
```

## Style

- Python 3.12, type hints required
- Linted with **ruff** — run `ruff check app/` before committing
- Imports sorted, no unused imports, no trailing whitespace
- Qt method overrides keep their Qt camelCase names
- Comments in English
- No `print()` — use the status bar

## Code of Conduct

Be respectful.
