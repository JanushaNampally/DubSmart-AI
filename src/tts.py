from gtts import gTTS
import os
import subprocess
def generate_tts(segments, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    audio_files = []

    for i, seg in enumerate(segments):
        speaker = seg["speaker"]

        slow = False
        if speaker.endswith("A"):
            slow = True  # aged
        elif speaker.endswith("B"):
            slow = False  # female-ish

        mp3 = os.path.join(output_dir, f"seg_{i}.mp3")
        wav = os.path.join(output_dir, f"seg_{i}.wav")

        gTTS(text=seg["text"], lang="te", slow=slow).save(mp3)

        subprocess.run([
            "ffmpeg", "-y",
            "-i", mp3,
            "-ar", "16000",
            "-ac", "1",
            wav
        ])

        audio_files.append(wav)

    return audio_files
