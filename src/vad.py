'''from pydub import AudioSegment
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



import torch
from silero_vad import get_speech_timestamps, read_audio, save_audio

def apply_vad(audio_path):
    """
    4.3 Noise Suppression (light)
    4.4 Voice Activity Detection
    """
    model, utils = torch.hub.load(
        repo_or_dir="snakers4/silero-vad",
        model="silero_vad",
        trust_repo=True
    )

    wav = read_audio(audio_path, sampling_rate=16000)
    timestamps = get_speech_timestamps(wav, model)

    clean_audio = "data/clean_audio.wav"
    save_audio(clean_audio, wav, timestamps)

    return clean_audio

'''
import soundfile as sf
from silero_vad import get_speech_timestamps
import torch

def apply_vad(audio_path):
    """
    4.3 Noise Suppression (light)
    4.4 Voice Activity Detection
    """
    model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-vad",
        model="silero_vad",
        trust_repo=True
    )

    wav, sr = sf.read(audio_path)
    if wav.ndim > 1:
        wav = wav.mean(axis=1)

    timestamps = get_speech_timestamps(wav, model, sampling_rate=sr)

    # Save trimmed audio (simple concat)
    cleaned = []
    for t in timestamps:
        cleaned.append(wav[t["start"]:t["end"]])

    clean_audio = "data/clean_audio.wav"
    sf.write(clean_audio, torch.cat([torch.tensor(c) for c in cleaned]).numpy(), sr)

    return clean_audio
