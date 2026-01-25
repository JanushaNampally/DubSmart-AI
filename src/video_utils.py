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

import ffmpeg

def merge_audio_with_video(video_path, audio_path, output_path):
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(audio_path)

    (
        ffmpeg
        .output(
            video.video,      # ONLY video stream
            audio.audio,      # ONLY dubbed audio
            output_path,
            vcodec="copy",
            acodec="aac",
            shortest=True
        )
        .overwrite_output()
        .run()
    )
