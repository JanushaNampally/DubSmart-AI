import whisper
import warnings
warnings.filterwarnings("ignore")

_model = whisper.load_model("small")

def transcribe(audio_path):
    return _model.transcribe(audio_path)["text"]
