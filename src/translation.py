# def translate(text, src="hi", tgt="en"):
    # Stable demo translation placeholder
    # English TTS is guaranteed to be audible
#   return text
'''
from deep_translator import GoogleTranslator


def translate_segments(segments, target_lang="te"):
    translator = GoogleTranslator(source="auto", target=target_lang)

    translated = []
    for seg in segments:
        translated_text = translator.translate(seg["text"])
        translated.append({
            "speaker": seg["speaker"],
            "start": seg["start"],
            "end": seg["end"],
            "text": translated_text
        })

    return translated
'''
from deep_translator import GoogleTranslator

def translate_segments(segments, target_lang="te"):
    translator = GoogleTranslator(source="auto", target=target_lang)

    translated = []
    for seg in segments:
        translated_text = translator.translate(seg["text"])
        translated.append({
            "speaker": seg["speaker"],
            "start": seg["start"],
            "end": seg["end"],
            "text": translated_text   # 👈 keep this consistent
        })

    return translated
