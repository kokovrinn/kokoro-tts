# -*- mode: python ; coding: utf-8 -*-
import os
import platform
import site
import subprocess
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# --- Version ---
# Priority: GITHUB_REF_NAME (CI) > git describe (local) > "0.0.0-dev"
version = os.environ.get("GITHUB_REF_NAME", "")
if version.startswith("v"):
    version = version[1:]
if not version:
    try:
        version = (
            subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True, text=True, timeout=5,
            )
            .stdout.strip()
            .lstrip("v")
        )
    except Exception:
        pass
if not version:
    version = "0.0.0-dev"

# Write version into app so About dialog shows the right number
Path("app/version.py").write_text(f'__version__ = "{version}"\n')

system = platform.system()
arch = platform.machine()
is_arm = arch in ("arm64", "aarch64")

venv_site = Path(site.getsitepackages()[0])
espeak_dir = venv_site / "espeakng_loader"

# espeak-ng library extension per platform
if system == "Windows":
    lib_ext = ".dll"
elif system == "Linux":
    lib_ext = ".so"
else:
    lib_ext = ".dylib"

espeak_lib = str(espeak_dir / f"libespeak-ng{lib_ext}")
espeak_data = str(espeak_dir / "espeak-ng-data")

# -----------------------------------
# PyInstaller hidden imports
# -----------------------------------
kokoro_hidden = collect_submodules("kokoro")
misaki_hidden = collect_submodules("misaki")
espeakng_hidden = collect_submodules("espeakng_loader")

datas = [
    (espeak_lib, "espeakng_loader"),
    (espeak_data, "espeakng_loader/espeak-ng-data"),
]
datas += collect_data_files("misaki")
datas += collect_data_files("espeakng_loader")

# -----------------------------------
# Excluded modules (save size)
# -----------------------------------
excluded = [
    "tkinter",
    "matplotlib",
    "notebook",
    "jupyter",
    "IPython",
    "pygments",
    "PIL",
]

# -----------------------------------
# Common hidden imports
# -----------------------------------
hidden = (
    kokoro_hidden
    + misaki_hidden
    + espeakng_hidden
    + [
        "kokoro",
        "kokoro.pipeline",
        "kokoro.model",
        "kokoro.modules",
        "kokoro.istftnet",
        "kokoro.custom_stft",
        "misaki",
        "misaki.en",
        "misaki.espeak",
        "espeakng_loader",
        "soundfile",
        "soundfile._soundfile",
        "numpy",
        "torch",
        "transformers",
        "huggingface_hub",
        "fitz",
        "spacy",
        "en_core_web_sm",
        "PySide6.QtMultimedia",
    ]
)

# -----------------------------------
# Icon
# -----------------------------------
icon_file = None
if system == "Darwin":
    icon_candidate = Path("kokoro-tts.icns")
    if icon_candidate.exists():
        icon_file = str(icon_candidate)
elif system == "Windows":
    icon_candidate = Path("kokoro-tts.ico")
    if icon_candidate.exists():
        icon_file = str(icon_candidate)

# -----------------------------------
# EXE / APP name
# -----------------------------------
app_name = "Kokoro TTS"
console_mode = False

# -----------------------------------
# PyInstaller Analysis
# -----------------------------------
a = Analysis(
    ["app/main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=console_mode,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

# -----------------------------------
# macOS: create .app bundle
# -----------------------------------
if system == "Darwin":
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name=app_name,
    )

    app = BUNDLE(
        coll,
        name=f"{app_name}.app",
        icon=icon_file,
        bundle_identifier="com.kokoro.tts",
        info_plist={
            "CFBundleDisplayName": app_name,
            "CFBundleDevelopmentRegion": "en",
            "CFBundleIdentifier": "com.kokoro.tts",
            "CFBundleVersion": version,
            "CFBundleShortVersionString": version,
            "NSHighResolutionCapable": True,
        },
    )
