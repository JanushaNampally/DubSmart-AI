import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def transcribe_with_speakers(audio_path):
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        punctuate=True,
        language_detection=True
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path, config)

    results = []

    for utterance in transcript.utterances:
        results.append({
            "speaker": f"Speaker {utterance.speaker}",
            "start": utterance.start / 1000,
            "end": utterance.end / 1000,
            "text": utterance.text
        })

    return results
