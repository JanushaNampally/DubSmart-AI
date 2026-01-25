from src.audio_extraction import extract_audio
from src.vad import apply_vad
from src.stt import transcribe
from src.translation import translate
from src.tts import generate_tts
from src.alignment import mux

VIDEO = "data/story.mp4"

RAW_AUDIO = "artifacts/audio/raw.wav"
TTS_AUDIO = "artifacts/tts/english.wav"
OUTPUT = "output/dubbed_english_video.mp4"

def run():
    # 4.2 Audio Extraction
    extract_audio(VIDEO, RAW_AUDIO)

    # 4.4 Voice Activity Detection
    chunks = apply_vad(RAW_AUDIO, "artifacts/vad")

    # 4.6 Speech-to-Text (Hindi)
    full_text = ""
    for c in chunks:
        full_text += " " + transcribe(c)

    # 4.8 Translation (Hindi → English)
    translated = translate(full_text, src="hi", tgt="en")

    # 4.10 Text-to-Speech (English)
    generate_tts(translated, TTS_AUDIO)

    # 4.11–4.13 Audio-Video Muxing
    mux(VIDEO, TTS_AUDIO, OUTPUT)

if __name__ == "__main__":
    run()
