LANGUAGES: dict[str, str] = {
    "a": "🇺🇸 American English · 11F 9M",
    "b": "🇬🇧 British English · 4F 4M",
    "e": "🇪🇸 Spanish · 1F 2M",
    "f": "🇫🇷 French · 1F",
    "h": "🇮🇳 Hindi · 2F 2M",
    "i": "🇮🇹 Italian · 1F 1M",
    "p": "🇧🇷 Brazilian Portuguese · 1F 2M",
    "j": "🇯🇵 Japanese · 4F 1M",
    "z": "🇨🇳 Mandarin Chinese · 4F 4M",
}

VOICES: dict[str, list[str]] = {
    "a": [
        "af_heart",
        "af_alloy",
        "af_aoede",
        "af_bella",
        "af_jessica",
        "af_kore",
        "af_nicole",
        "af_nova",
        "af_river",
        "af_sarah",
        "af_sky",
        "am_adam",
        "am_echo",
        "am_eric",
        "am_fenrir",
        "am_liam",
        "am_michael",
        "am_onyx",
        "am_puck",
        "am_santa",
    ],
    "b": [
        "bf_alice",
        "bf_emma",
        "bf_isabella",
        "bf_lily",
        "bm_daniel",
        "bm_fable",
        "bm_george",
        "bm_lewis",
    ],
    "e": [
        "ef_dora",
        "em_alex",
        "em_santa",
    ],
    "f": [
        "ff_siwis",
    ],
    "h": [
        "hf_alpha",
        "hf_beta",
        "hm_omega",
        "hm_psi",
    ],
    "i": [
        "if_sara",
        "im_nicola",
    ],
    "p": [
        "pf_dora",
        "pm_alex",
        "pm_santa",
    ],
    "j": [
        "jf_alpha",
        "jf_gongitsune",
        "jf_nezumi",
        "jf_tebukuro",
        "jm_kumo",
    ],
    "z": [
        "zf_xiaobei",
        "zf_xiaoni",
        "zf_xiaoxiao",
        "zf_xiaoyi",
        "zm_yunjian",
        "zm_yunxi",
        "zm_yunxia",
        "zm_yunyang",
    ],
}

VOICE_INFO: dict[str, str] = {
    "af_heart": "Heart (F) · ★ A",
    "af_alloy": "Alloy (F) · ★ C",
    "af_aoede": "Aoede (F) · ★ C+",
    "af_bella": "Bella (F) · ★ A-",
    "af_jessica": "Jessica (F) · ★ D",
    "af_kore": "Kore (F) · ★ C+",
    "af_nicole": "Nicole (F) · ★ B-",
    "af_nova": "Nova (F) · ★ C",
    "af_river": "River (F) · ★ D",
    "af_sarah": "Sarah (F) · ★ C+",
    "af_sky": "Sky (F) · ★ C-",
    "am_adam": "Adam (M) · ★ F+",
    "am_echo": "Echo (M) · ★ D",
    "am_eric": "Eric (M) · ★ D",
    "am_fenrir": "Fenrir (M) · ★ C+",
    "am_liam": "Liam (M) · ★ D",
    "am_michael": "Michael (M) · ★ C+",
    "am_onyx": "Onyx (M) · ★ D",
    "am_puck": "Puck (M) · ★ C+",
    "am_santa": "Santa (M) · ★ D-",
    "bf_alice": "Alice (F) · ★ D",
    "bf_emma": "Emma (F) · ★ B-",
    "bf_isabella": "Isabella (F) · ★ C",
    "bf_lily": "Lily (F) · ★ D",
    "bm_daniel": "Daniel (M) · ★ D",
    "bm_fable": "Fable (M) · ★ C",
    "bm_george": "George (M) · ★ C",
    "bm_lewis": "Lewis (M) · ★ D+",
    "ef_dora": "Dora (F)",
    "em_alex": "Alex (M)",
    "em_santa": "Santa (M)",
    "ff_siwis": "Siwis (F) · ★ B-",
    "hf_alpha": "Alpha (F) · ★ C",
    "hf_beta": "Beta (F) · ★ C",
    "hm_omega": "Omega (M) · ★ C",
    "hm_psi": "Psi (M) · ★ C",
    "if_sara": "Sara (F) · ★ C",
    "im_nicola": "Nicola (M) · ★ C",
    "pf_dora": "Dora (F)",
    "pm_alex": "Alex (M)",
    "pm_santa": "Santa (M)",
    "jf_alpha": "Alpha (F) · ★ C+",
    "jf_gongitsune": "Gongitsune (F) · ★ C",
    "jf_nezumi": "Nezumi (F) · ★ C-",
    "jf_tebukuro": "Tebukuro (F) · ★ C",
    "jm_kumo": "Kumo (M) · ★ C-",
    "zf_xiaobei": "Xiaobei (F) · ★ D",
    "zf_xiaoni": "Xiaoni (F) · ★ D",
    "zf_xiaoxiao": "Xiaoxiao (F) · ★ D",
    "zf_xiaoyi": "Xiaoyi (F) · ★ D",
    "zm_yunjian": "Yunjian (M) · ★ D",
    "zm_yunxi": "Yunxi (M) · ★ D",
    "zm_yunxia": "Yunxia (M) · ★ D",
    "zm_yunyang": "Yunyang (M) · ★ D",
}

REPO_ID = "hexgrad/Kokoro-82M"

ALL_VOICES = [
    # American
    "af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica", "af_kore", "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael", "am_onyx", "am_puck", "am_santa",
    # British
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
    # Spanish
    "ef_dora", "em_alex", "em_santa",
    # French
    "ff_siwis",
    # Hindi
    "hf_alpha", "hf_beta", "hm_omega", "hm_psi",
    # Italian
    "if_sara", "im_nicola",
    # Portuguese
    "pf_dora", "pm_alex", "pm_santa",
    # Japanese
    "jf_alpha", "jf_gongitsune", "jf_nezumi", "jf_tebukuro", "jm_kumo",
    # Mandarin
    "zf_xiaobei", "zf_xiaoni", "zf_xiaoxiao", "zf_xiaoyi", "zm_yunjian", "zm_yunxi", "zm_yunxia", "zm_yunyang"
]

_cached_voices: list[str] | None = None

def get_all_voices() -> list[str]:
    global _cached_voices
    if _cached_voices is not None:
        return _cached_voices

    try:
        from huggingface_hub import list_repo_files
        files = list_repo_files(REPO_ID)
        voices = [f[7:-3] for f in files if f.startswith("voices/") and f.endswith(".pt")]
        if voices:
            _cached_voices = sorted(voices)
            return _cached_voices
    except Exception:
        pass

    _cached_voices = ALL_VOICES
    return _cached_voices

def get_voice_display_name(voice: str) -> str:
    if voice in VOICE_INFO:
        return f"{voice} — {VOICE_INFO[voice]}"

    parts = voice.split("_")
    if len(parts) == 2:
        prefix, name = parts
        gender = "F" if prefix.endswith("f") else "M"
        lang = LANGUAGES.get(prefix[:1], "Unknown")
        return f"{voice} — {name.title()} ({gender}) [{lang}]"
    return voice
