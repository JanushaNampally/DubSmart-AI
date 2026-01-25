'''from src.audio_extraction import extract_audio
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

from src.audio_extraction import extract_audio
from src.vad import apply_vad
from src.stt import transcribe_with_speakers
from src.alignment import segment_text
from src.translation import translate_segments
from src.tts import generate_tts
from src.video_utils import merge_audio_with_video
import os

VIDEO_PATH = "data/story.mp4"
OUTPUT_VIDEO = "output/dubbed_video.mp4"

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# 4.1 Extract audio
audio_path = extract_audio(VIDEO_PATH)

# 4.2 Voice Activity Detection
clean_audio = apply_vad(audio_path)

# 4.3–4.5 STT + Speaker Diarization
segments = transcribe_with_speakers(clean_audio)

# 4.6–4.7 Text segmentation & alignment
segments = segment_text(segments)

# 4.8 Translation
translated_segments = translate_segments(segments)

# 4.9–4.10 TTS
dubbed_audio_path = generate_tts(translated_segments)

# 4.11–4.13 Merge audio with video
merge_audio_with_video(
    video_path=VIDEO_PATH,
    audio_path=dubbed_audio_path,
    output_path=OUTPUT_VIDEO
)

print("inal dubbed video generated:", OUTPUT_VIDEO)
'''
from src.audio_extraction import extract_audio
from src.vad import apply_vad
from src.stt import transcribe_with_speakers
from src.alignment import segment_text, create_final_audio
from src.translation import translate_segments
from src.tts import generate_tts
from src.video_utils import merge_audio_with_video
import os

VIDEO_PATH = "data/story.mp4"
OUTPUT_VIDEO = "output/dubbed_video.mp4"

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# 4.1–4.2 Extract audio
audio_path = extract_audio(VIDEO_PATH)

# 4.3–4.4 Voice Activity Detection
clean_audio = apply_vad(audio_path)

# 4.5–4.6 STT + Speaker Diarization
segments = transcribe_with_speakers(clean_audio)

# 4.7 Text segmentation & alignment
segments = segment_text(segments)

# 4.8 Translation
translated_segments = translate_segments(segments)
print(translated_segments[0])  # debug print (safe)

# 4.9–4.10 Text-to-Speech
tts_files = generate_tts(translated_segments)

# 4.11–4.12 Audio concatenation
final_audio = create_final_audio(tts_files)

# 4.13 Merge dubbed audio with video
merge_audio_with_video(
    video_path=VIDEO_PATH,
    audio_path=final_audio,
    output_path=OUTPUT_VIDEO
)

print("Final dubbed video generated:", OUTPUT_VIDEO)
