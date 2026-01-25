from gtts import gTTS
import os

def generate_tts(text, out_path="artifacts/tts/english.wav"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Use actual transcribed / translated text
    cleaned_text = text.strip()

    # Safety fallback (only if transcription is empty)
    if len(cleaned_text) < 5:
        cleaned_text = "This is an English dubbed audio generated from the original Hindi video."

    tts = gTTS(text=cleaned_text, lang="en", slow=False)
    tts.save(out_path)

    return out_path
