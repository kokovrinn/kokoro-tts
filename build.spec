# -*- mode: python ; coding: utf-8 -*-
import site
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

venv_site = Path(site.getsitepackages()[0])

espeak_lib = str(venv_site / "espeakng_loader/libespeak-ng.dylib")
espeak_data = str(venv_site / "espeakng_loader/espeak-ng-data")

kokoro_hidden = collect_submodules("kokoro")
misaki_hidden = collect_submodules("misaki")
espeakng_hidden = collect_submodules("espeakng_loader")

added_files = [
    (espeak_lib, "espeakng_loader"),
    (espeak_data, "espeakng_loader/espeak-ng-data"),
]

added_files += collect_data_files("misaki")
added_files += collect_data_files("espeakng_loader")

excluded = [
    "tkinter",
    "matplotlib",
    "notebook",
    "jupyter",
    "IPython",
    "pygments",
    "PIL",
]

a = Analysis(
    ["app/main.py"],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=kokoro_hidden + misaki_hidden + espeakng_hidden + [
        "kokoro", "kokoro.pipeline", "kokoro.model", "kokoro.modules",
        "kokoro.istftnet", "kokoro.custom_stft",
        "misaki", "misaki.en", "misaki.espeak",
        "espeakng_loader",
        "soundfile", "soundfile._soundfile",
        "numpy", "torch", "transformers",
        "huggingface_hub", "fitz",
        "spacy", "en_core_web_sm",
        "PySide6.QtMultimedia",
    ],
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
    name="Kokoro TTS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="kokoro-tts.icns",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Kokoro TTS",
)

app_bundle = BUNDLE(
    coll,
    name="Kokoro TTS.app",
    icon="kokoro-tts.icns",
    bundle_identifier="com.kokoro.tts",
)
