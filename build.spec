# -*- mode: python ; coding: utf-8 -*-
import os
import platform
import site
import subprocess
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# --- Version ---
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

Path("app/version.py").write_text(f'__version__ = "{version}"\n')

system = platform.system()

# --- espeak-ng library (use the package's own resolver) ---
from espeakng_loader import get_library_path, get_data_path

espeak_lib = get_library_path()
espeak_data = get_data_path()

# --- PyInstaller hidden imports ---
kokoro_hidden = collect_submodules("kokoro")
misaki_hidden = collect_submodules("misaki")
espeakng_hidden = collect_submodules("espeakng_loader")

datas = [
    (espeak_lib, "espeakng_loader"),
    (espeak_data, "espeakng_loader/espeak-ng-data"),
]
datas += collect_data_files("misaki")
datas += collect_data_files("espeakng_loader")

excluded = [
    "tkinter",
    "matplotlib",
    "notebook",
    "jupyter",
    "IPython",
    "pygments",
    "PIL",
    "nvidia",
    "torch._dynamo",
    "torch._inductor",
    "torch.distributed",
    "torch.profiler",
    "torch.onnx",
    "torch.backends.mps",
]

hidden = (
    kokoro_hidden
    + misaki_hidden
    + espeakng_hidden
    + [
        "kokoro", "kokoro.pipeline", "kokoro.model", "kokoro.modules",
        "kokoro.istftnet", "kokoro.custom_stft",
        "misaki", "misaki.en", "misaki.espeak",
        "espeakng_loader",
        "soundfile",
        "numpy", "torch", "transformers",
        "huggingface_hub", "fitz",
        "spacy",
        "PySide6.QtMultimedia",
    ]
)

# --- Icon ---
icon_file = None
if system == "Darwin":
    cand = Path("kokoro-tts.icns")
    if cand.exists():
        icon_file = str(cand)
elif system == "Windows":
    cand = Path("kokoro-tts.ico")
    if cand.exists():
        icon_file = str(cand)

app_name = "Kokoro TTS"

# --- Analysis ---
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
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name=app_name,
)

# --- macOS: .app bundle ---
if system == "Darwin":
    BUNDLE(
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
