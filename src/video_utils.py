'''import ffmpeg

def merge_audio_with_video(video_path, audio_path, output_path):
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(audio_path)

    (
        ffmpeg
        .output(video.video, audio.audio, output_path, vcodec="copy", acodec="aac")
        .overwrite_output()
        .run()
    )
'''
import subprocess
import os

def merge_audio_with_video(video_path, audio_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-shortest",
        output_path
    ]

    subprocess.run(command, check=True)

    return output_path
