'''import subprocess
import os

def mux(video_path, audio_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    subprocess.run(command, check=True)
    return output_path

import ffmpeg
def segment_text(segments):
    """
    4.7 Text Segmentation & Alignment
    """
    aligned = []
    for seg in segments:
        aligned.append({
            "text": seg["text"],
            "start": seg["start"],
            "end": seg["end"]
        })
    return aligned

def create_final_video(video_path, audio_files):
    """
    4.11 Prosody & Timing (approx)
    4.12 Audio Mixing
    4.13 Final Dubbed Output
    """
    concat_audio = "outputs/final_audio.mp3"

    with open("outputs/audio_list.txt", "w") as f:
        for a in audio_files:
            f.write(f"file '{a}'\n")

    ffmpeg.input("outputs/audio_list.txt", format="concat", safe=0)\
        .output(concat_audio)\
        .overwrite_output()\
        .run(quiet=True)

    ffmpeg.input(video_path).output(
        "outputs/dubbed_telugu.mp4",
        audio=concat_audio
    ).overwrite_output().run(quiet=True)

'''
import ffmpeg
import os

def segment_text(segments):
    """
    4.6–4.7 Text Segmentation & Alignment
    """
    aligned = []
    for seg in segments:
        aligned.append({
            "speaker": seg.get("speaker", "Speaker"),
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })
    return aligned


def create_final_audio(audio_files):
    """
    4.11 Prosody & Timing (approx)
    4.12 Audio Mixing
    4.13 Final Dubbed Output
    """

    os.makedirs("outputs", exist_ok=True)
    final_audio = "outputs/final_audio.wav"

    inputs = [ffmpeg.input(f) for f in audio_files]

    (
        ffmpeg
        .concat(*inputs, v=0, a=1)
        .output(final_audio, ac=1, ar=16000)
        .overwrite_output()
        .run(quiet=True)
    )

    return final_audio
