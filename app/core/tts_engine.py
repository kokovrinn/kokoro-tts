from collections.abc import Generator

from PySide6.QtCore import QObject, Signal


class TTSEngine(QObject):
    synthesis_started = Signal()
    synthesis_progress = Signal(str)
    synthesis_finished = Signal(str, object)
    synthesis_error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pipeline = None
        self._current_lang = None

    def _ensure_pipeline(self, lang_code: str):
        if self._pipeline is None or self._current_lang != lang_code:
            self.synthesis_progress.emit("Loading TTS model…")
            from kokoro import KPipeline
            self._pipeline = KPipeline(lang_code=lang_code)
            self._current_lang = lang_code

    def synthesize(
        self, text: str, voice: str, speed: float = 1.0,
        lang_code: str | None = None
    ):
        if lang_code is None:
            lang_code = voice[:1]
        try:
            self.synthesis_started.emit()
            self._ensure_pipeline(lang_code)

            self.synthesis_progress.emit("Converting text to speech…")
            generator: Generator = self._pipeline(
                text, voice=voice, speed=speed
            )

            all_audio = []
            for i, (gs, ps, audio) in enumerate(generator):
                if audio is not None:
                    all_audio.append(audio)
                self.synthesis_progress.emit(
                    f"Processing segment {i + 1}…"
                )

            if not all_audio:
                raise RuntimeError("No audio generated.")

            import torch
            combined = torch.cat(all_audio) if len(all_audio) > 1 else all_audio[0]

            self.synthesis_finished.emit(text, combined)
        except Exception as e:
            self.synthesis_error.emit(str(e))

    def save_audio(self, audio, output_path: str):
        import soundfile as sf
        audio_np = audio.detach().cpu().numpy()
        if audio_np.ndim > 1:
            audio_np = audio_np.squeeze()
        audio_int16 = (audio_np * 32767).astype("int16")
        sf.write(output_path, audio_int16, 24000)
