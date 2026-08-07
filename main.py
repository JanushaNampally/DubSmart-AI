from src.audio_extraction import extract_audio, _validate_video
from src.vad import apply_vad
from src.stt import transcribe_with_speakers
from src.alignment import segment_text, create_final_audio
from src.translation import translate_segments
from src.tts import generate_tts
from src.video_utils import merge_audio_with_video
import os
import sys

# Paths
VIDEO_PATH = "data/story.mp4"
OUTPUT_VIDEO = "output/dubbed_video.mp4"
JOB_DIR = "artifacts/job"

# Ensure directories exist
os.makedirs("output", exist_ok=True)
os.makedirs(JOB_DIR, exist_ok=True)


def run():
    """Run the full dubbing pipeline."""
    try:
        log("=" * 50)
        log("DubSmart AI Pipeline Starting...")
        log("=" * 50)

        # 4.1–4.2 Extract audio (with video validation)
        audio_path = extract_audio(video_path=VIDEO_PATH, output_dir=JOB_DIR)
        log(f"✓ Audio extracted: {audio_path}")

        # 4.3–4.4 Voice Activity Detection
        clean_audio = apply_vad(audio_path=audio_path, output_dir=JOB_DIR)
        log(f"✓ VAD applied: {clean_audio}")

        # 4.5–4.6 STT + Speaker Diarization
        segments = transcribe_with_speakers(clean_audio)
        log(f"✓ Transcription: {len(segments)} segments, speakers: {set(s['speaker'] for s in segments)}")

        # 4.7 Text segmentation & alignment
        segments = segment_text(segments)
        log(f"✓ Segmented: {len(segments)} segments after filtering")

        # 4.8 Translation
        translated_segments = translate_segments(segments)
        log(f"✓ Translated to Telugu")

        # 4.9–4.10 Text-to-Speech (voice cloning from clean audio)
        tts_files = generate_tts(translated_segments, output_dir=JOB_DIR, audio_path=clean_audio)
        log(f"✓ TTS generated: {len(tts_files)} audio files")

        # 4.11–4.12 Audio concatenation
        final_audio = create_final_audio(tts_files, output_dir=JOB_DIR)
        log(f"✓ Audio stitched: {final_audio}")

        # 4.13 Merge dubbed audio with video
        merge_audio_with_video(
            video_path=VIDEO_PATH,
            audio_path=final_audio,
            output_path=OUTPUT_VIDEO
        )

        log("=" * 50)
        log(f"SUCCESS: Dubbed video -> {OUTPUT_VIDEO}")
        log("=" * 50)
    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(1)
def log(msg):
    print(msg)
if __name__ == "__main__":
    if not os.path.exists(VIDEO_PATH):
        print(f"Video file not found: {VIDEO_PATH}")
        print("   Please place your input video at 'data/story.mp4'")
        print("   OR upload a video through the web app (python webapp/manage.py runserver)")
        sys.exit(1)

    try:
        _validate_video(VIDEO_PATH)
    except ValueError as e:
        print(f"{e}")
        print("\nThe repo contains Git LFS pointer files instead of actual videos.")
        print("   To fix this, either:")
        print("   1. Run 'git lfs pull' to download the real video files")
        print("   2. Or delete the pointer files and place your own .mp4 in the data/ folder")
        print("   3. Or use the web app at http://127.0.0.1:8000/ to upload a video")
        sys.exit(1)

    run()
