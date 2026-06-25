"""
speak.py — turn the digest text into an MP3 using Piper (free, cloud-friendly).

Piper is a neural text-to-speech engine that runs on the GitHub runner with no
API key and no cost. We render to WAV, then compress to a small MP3 with ffmpeg.
Only used in the cloud (the workflow installs piper + ffmpeg).
"""

import os
import subprocess
import tempfile

from digest import markdown_to_speech_text  # reuse the markdown→spoken cleanup

# Path to the downloaded Piper voice model (set in the workflow).
PIPER_MODEL = os.environ.get("PIPER_MODEL", "voice/en_US-lessac-medium.onnx")


def make_mp3(text, out_mp3):
    os.makedirs(os.path.dirname(out_mp3), exist_ok=True)
    speech = markdown_to_speech_text(text)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav = tmp.name

    # Piper reads the text on stdin and writes a WAV file.
    subprocess.run(
        ["piper", "--model", PIPER_MODEL, "--output_file", wav],
        input=speech.encode("utf-8"),
        check=True,
    )
    # Compress to a small mono MP3 (plenty for speech).
    subprocess.run(
        ["ffmpeg", "-y", "-i", wav, "-ac", "1", "-b:a", "64k", out_mp3],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.remove(wav)
    return out_mp3
