from moviepy import VideoFileClip
import os

def extract_audio(video_path):
    """
    4.1 Source Video Input
    4.2 Audio Extraction
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError("Input video not found")

    clip = VideoFileClip(video_path)
    audio_path = "data/extracted_audio.wav"
    clip.audio.write_audiofile(audio_path, fps=16000, nbytes=2, codec="pcm_s16le")
    return audio_path
