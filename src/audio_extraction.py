import os
from moviepy import VideoFileClip


def extract_audio(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "extracted_audio.wav")

    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(
        audio_path,
        fps=16000,
        codec="pcm_s16le"
    )
    clip.close()

    return audio_path
