'''# src/pipeline.py

from pathlib import Path
import shutil

from src.audio_extraction import extract_audio
from src.vad import apply_vad
from src.stt import transcribe_with_speakers
from src.alignment import segment_text, create_final_audio
from src.translation import translate_segments
from src.tts import generate_tts
from src.video_utils import merge_audio_with_video


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
MEDIA_DIR = BASE_DIR / "media"

DATA_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)


def run_pipeline(log):
    video_path = DATA_DIR / "input.mp4"

    log(f"Checking input video at: {video_path}")

    if not video_path.exists():
        log("ERROR: input.mp4 NOT FOUND")
        return None

    log(f"Video file size: {video_path.stat().st_size} bytes")

    final_output_video = OUTPUTS_DIR / "dubbed_output.mp4"
    media_video = MEDIA_DIR / "dubbed_output.mp4"

    # ---------------- AUDIO EXTRACTION ----------------
    log("Extracting audio...")
    try:
        audio_path = extract_audio(str(video_path))
        log(f"Audio extracted to: {audio_path}")
    except Exception as e:
        log(f"ERROR during audio extraction: {e}")
        return None

    # ---------------- VAD ----------------
    log("Applying VAD...")
    clean_audio = apply_vad(audio_path)

    # ---------------- STT ----------------
    log("Speech to text...")
    segments = transcribe_with_speakers(clean_audio)
    log(f"STT segments detected: {len(segments)}")

    # ---------------- ALIGN + TRANSLATE ----------------
    log("Aligning text...")
    aligned_segments = segment_text(segments)

    log("Translating...")
    translated_segments = translate_segments(aligned_segments)

    # ---------------- TTS ----------------
    log("Generating TTS...")
    tts_files = generate_tts(translated_segments)

    log("Creating final audio...")
    final_audio = create_final_audio(tts_files)

    # ---------------- MERGE ----------------
    log("Merging audio + video...")
    try:
        merge_audio_with_video(
            video_path=str(video_path),
            audio_path=final_audio,
            output_path=str(final_output_video)
        )

        # Copy final video to Django media folder
        shutil.copy(final_output_video, media_video)

        log("Video merge completed successfully")

    except Exception as e:
        log(f"ERROR while merging video: {e}")
        return None

    log("DONE")

    # Django-served path
    return "/media/dubbed_output.mp4"

# src/pipeline.py
# src/pipeline.py

import os
from django.conf import settings

from src.audio_extraction import extract_audio
from src.vad import apply_vad
from src.stt import transcribe_with_speakers
from src.alignment import segment_text, create_final_audio
from src.translation import translate_segments
from src.tts import generate_tts
from src.video_utils import merge_audio_with_video


PIPELINE_STATUS = {
    "running": False,
    "done": False,
    "output": None
}


def log(msg):
    print(msg)

def start(request):
    ...
    job_dir = os.path.join(settings.MEDIA_ROOT, "jobs", "job_001")
    os.makedirs(job_dir, exist_ok=True)

    input_path = os.path.join(job_dir, "input.mp4")

def run_pipeline(input_video, output_dir, log_callback):
    try:
        PIPELINE_STATUS.update({
            "running": True,
            "done": False,
            "output": None
        })

        input_video = os.path.join(settings.MEDIA_ROOT, "input.mp4")
        output_video = os.path.join(settings.MEDIA_ROOT, "dubbed_output.mp4")

        log("Checking input video...")
        audio = extract_audio(input_video)
        log_callback("Extracting audio...")

        log("Applying VAD...")
        clean_audio = apply_vad(audio)

        log("Speech to text...")
        segments = transcribe_with_speakers(clean_audio)
        if not segments:
            raise RuntimeError("No speech segments detected")

        for seg in segments:
            log(f"{seg['speaker']}: {seg['text']}")

        log("Aligning text...")
        aligned = segment_text(segments)

        log("Translating...")
        translated = translate_segments(aligned)

        log("Generating TTS...")
        tts_files = generate_tts(translated)

        log("Creating final audio...")
        final_audio = create_final_audio(tts_files)

        log("Merging audio + video...")
        merge_audio_with_video(
            video_path=input_video,
            audio_path=final_audio,
            output_path=output_video
        )

        PIPELINE_STATUS.update({
            "running": False,
            "done": True,
            "output": settings.MEDIA_URL + "dubbed_output.mp4"
        })

        log("DONE")

    except Exception as e:
        PIPELINE_STATUS["running"] = False
        log(f"❌ ERROR: {str(e)}")
'''
# src/pipeline.py


# src/pipeline.py

import os
from src.audio_extraction import extract_audio
from src.vad import apply_vad
from src.stt import transcribe_with_speakers
from src.alignment import segment_text, create_final_audio
from src.translation import translate_segments
from src.tts import generate_tts
from src.video_utils import merge_audio_with_video

def run_pipeline(input_video, job_dir, log):
    try:
        log("Checking input video...")

        log("Extracting audio...")
        audio_path = extract_audio(
            video_path=input_video,
            output_dir=job_dir
        )

        log("Applying VAD...")
        clean_audio = apply_vad(
            audio_path=audio_path,
            output_dir=job_dir
        )

        log("Speech to text...")
        segments = transcribe_with_speakers(clean_audio)

        for seg in segments:
            log(f"{seg['speaker']}: {seg['text']}")

        log("Aligning text...")
        segments = segment_text(segments)

        log("Translating...")
        translated = translate_segments(segments)

        log("Generating TTS...")
        tts_files = generate_tts(
            translated,
            output_dir=job_dir
        )

        log("Merging audio + video...")
        final_audio = create_final_audio(
            tts_files,
            output_dir=job_dir
        )

        output_video = os.path.join(job_dir, "dubbed.mp4")
        merge_audio_with_video(
            video_path=input_video,
            audio_path=final_audio,
            output_path=output_video
        )

        log("DONE")
        return output_video

    except Exception as e:
        log(f"ERROR: {str(e)}")
        return None
