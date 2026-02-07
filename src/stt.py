import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_with_speakers(audio_path):
    config = aai.TranscriptionConfig(
    language_code="hi",
    speaker_labels=True,
    punctuate=True
)


    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path, config)

    if not transcript.utterances:
        raise RuntimeError("No speech detected")

    results = []
    for utt in transcript.utterances:
        results.append({
            "speaker": f"Speaker {utt.speaker}",
            "start": utt.start / 1000,
            "end": utt.end / 1000,
            "text": utt.text
        })

    return results
