# DubSmart AI — Intelligent Video Dubbing with Voice Cloning

DubSmart AI is an end-to-end video dubbing pipeline that automatically replaces the original speech in a video with a translated, voice-cloned narration. It converts Hindi speech to natural-sounding Telugu while preserving the original speaker's voice characteristics.

## Features

- **Audio Extraction** — Extracts audio track from input video
- **Voice Activity Detection (VAD)** — Removes silence/non-speech segments
- **Speech-to-Text (STT) + Speaker Diarization** — Transcribes Hindi speech with speaker labels using AssemblyAI
- **Translation** — Converts Hindi segments to Telugu using Google Translator
- **Voice Cloning TTS** — Generates Telugu speech with Coqui XTTS-v2, matching each speaker's original voice
- **Audio Alignment & Concatenation** — Stitches TTS segments into a continuous audio track
- **Video Merging** — Combines dubbed audio with original video

## Pipeline Architecture

```
Input Video (.mp4)
    │
    ▼
┌─────────────────────┐
│ Audio Extraction    │  src/audio_extraction.py
│ (moviepy → .wav)   │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Voice Activity      │  src/vad.py
│ Detection (pydub)   │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ STT + Speaker       │  src/stt.py
│ Diarization         │  (AssemblyAI)
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Text Segmentation   │  src/alignment.py
│ & Filtering         │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Translation         │  src/translation.py
│ (Hindi → Telugu)    │  (deep-translator)
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ TTS + Voice Cloning │  src/tts.py
│ (Coqui XTTS-v2)     │  (Telugu, per-speaker)
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Audio Concatenation │  src/alignment.py
│ (ffmpeg concat)     │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Merge Audio+Video   │  src/video_utils.py
│ (ffmpeg)            │
└─────────┬───────────┘
          ▼
    Dubbed Video (.mp4)
```

## Project Structure

```
DubSmart-AI/
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── .env                     # API keys (ASSEMBLYAI_API_KEY)
├── .gitignore
├── .gitattributes
│
├── src/
│   ├── audio_extraction.py  # Extract audio from video
│   ├── vad.py               # Voice Activity Detection
│   ├── stt.py               # Speech-to-Text + Speaker Diarization
│   ├── translation.py       # Hindi → Telugu translation
│   ├── tts.py               # Text-to-Speech with voice cloning
│   ├── alignment.py         # Segment filtering & audio concatenation
│   ├── video_utils.py       # Merge dubbed audio with video
│   └── pipeline.py          # Orchestrates the full pipeline
│
├── webapp/                  # Django web application (optional UI)
├── data/                    # Input video files (e.g., story.mp4)
├── artifacts/               # Intermediate outputs (auto-created)
├── output/                  # Final dubbed video (auto-created)
│
├── DubSmart AI.pptx         # Presentation
└── PBL_Review DubsmartAI.docx  # Project report
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- FFmpeg installed and available in PATH
- AssemblyAI API key

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd DubSmart-AI

# 2. Create and activate virtual environment
python -m venv myenv
# Windows:
myenv\Scripts\activate
# Linux/Mac:
source myenv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file with:
echo ASSEMBLYAI_API_KEY=your_key_here > .env
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `numpy` | Numerical computing |
| `soundfile` | Audio file I/O |
| `moviepy` | Video/audio processing |
| `ffmpeg-python` | FFmpeg bindings |
| `pydub` | Audio segment manipulation |
| `assemblyai` | STT + Speaker Diarization |
| `deep-translator` | Hindi → Telugu translation |
| `python-dotenv` | Environment variable management |
| `TTS` (Coqui XTTS-v2) | Voice cloning TTS |
| `torch` + `torchaudio` | PyTorch backend for TTS |

## Usage

### Run the Pipeline (CLI)

```bash
python main.py
```

The pipeline will:
1. Read input video from `data/story.mp4` (configurable in `main.py`)
2. Process through all stages
3. Output the final dubbed video to `output/dubbed_video.mp4`

### Run via Web App

```bash
cd webapp
python manage.py runserver
```

### Configuration

- **Input video path**: Edit `VIDEO_PATH` in `main.py`
- **Output path**: Edit `OUTPUT_VIDEO` in `main.py`
- **Source language**: Edit `language_code` in `src/stt.py` (default: `"hi"` for Hindi)
- **Target language**: Edit `target_lang` in `src/translation.py` (default: `"te"` for Telugu)

## Voice Cloning Implementation

The TTS module (`src/tts.py`) uses Coqui XTTS-v2 for multilingual voice cloning:

1. **Speaker Detection** — STT returns speaker labels with timestamps per segment
2. **Voice Reference Extraction** — For each unique speaker, extracts a 2–10 second voice sample from the cleaned audio using their first segment's timestamps
3. **Voice-Cloned Generation** — Generates Telugu TTS using the extracted voice reference
4. **Fallback** — If voice extraction fails (e.g., no timestamps), falls back to XTTS's default speaker
5. **Error Resilience** — Failing segments generate a silent placeholder to maintain audio alignment

### Key Details

- **Model**: `tts_models/multilingual/multi-dataset/xtts_v2` (downloaded once on first run)
- **Device**: Auto-detects CUDA GPU; falls back to CPU
- **Language**: Telugu (`"te"`) for output speech
- **Sample Rate**: 16kHz mono WAV output

## Troubleshooting

### Import Errors

| Error | Solution |
|-------|----------|
| `No module named 'torchaudio'` | Install torchaudio: `pip install torchaudio` |
| `No module named 'proglog'` | Install proglog: `pip install proglog` |
| `No module named 'silero_vad'` | Not required (VAD uses pydub instead) |
| `pkg_resources` import error | Downgrade setuptools: `pip install 'setuptools<75'` |

### Model Download

The Coqui XTTS-v2 model (~2GB) is downloaded automatically on first TTS generation. Ensure a stable internet connection.

## Implementation History

- Analyzed codebase — STT returns speaker labels + timestamps; gTTS replaced with Coqui XTTS-v2
- Rewrote `src/tts.py` — Added Coqui XTTS-v2 with auto GPU/CPU detection, voice reference extraction, Telugu TTS generation, and fallback handling
- Updated `src/pipeline.py` — Passes `audio_path` (clean_audio) for voice cloning
- Updated `main.py` — Passes `clean_audio` for voice cloning
- Updated `requirements.txt` — Added `TTS`, `torch`, `torchaudio` dependencies
- Verified module imports — All source modules import correctly

---

*DubSmart AI — AI-powered video dubbing with speaker voice preservation*

