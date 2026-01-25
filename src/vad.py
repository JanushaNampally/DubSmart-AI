from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def apply_vad(audio_path, out_dir):
    audio = AudioSegment.from_wav(audio_path)
    chunks = split_on_silence(audio, min_silence_len=500, silence_thresh=-40)

    paths = []
    for i, chunk in enumerate(chunks):
        path = os.path.join(out_dir, f"chunk_{i}.wav")
        chunk.export(path, format="wav")
        paths.append(path)

    return paths
