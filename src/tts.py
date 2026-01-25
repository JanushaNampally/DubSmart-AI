'''from gtts import gTTS
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

from gtts import gTTS

def generate_tts(segments):
    """
    4.9 Voice Selection
    4.10 Text to Speech
    """
    audio_files = []

    for i, seg in enumerate(segments):
        tts = gTTS(seg["translated"], lang="te")
        out = f"outputs/seg_{i}.mp3"
        tts.save(out)
        audio_files.append(out)

    return audio_files
'''
from gtts import gTTS
import os

def generate_tts(segments):
    """
    4.9 Voice Selection
    4.10 Text to Speech
    """
    os.makedirs("outputs", exist_ok=True)
    audio_files = []

    for i, seg in enumerate(segments):
        # Handle both possible keys safely
        text = seg.get("text") or seg.get("translated")

        if not text:
            raise ValueError(f"No text found for TTS in segment {i}: {seg}")

        tts = gTTS(text, lang="te")
        out = f"outputs/seg_{i}.mp3"
        tts.save(out)
        audio_files.append(out)

    return audio_files
