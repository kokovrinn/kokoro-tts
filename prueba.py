from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code='e')

text = "Hola, esta es una prueba de Kokoro TTS."

generator = pipeline(text, voice='af_bella')

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f"salida_{i}.wav", audio, 24000)
    break