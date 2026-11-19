"""
speak.py — turn the digest text into an MP3 using Kokoro (free, open-source TTS).

Kokoro is a small neural voice model (Apache-2.0) that runs on the GitHub
runner with no API key and no cost. It renders 24 kHz audio, which ffmpeg
compresses to a small mono MP3. Voice: George (British male).

Try it locally:  python speak.py digests/2026-11-19/ai.md /tmp/test.mp3
"""

import os
import subprocess
import sys
import tempfile

# Kokoro's helper package ships its own espeak-ng build, whose data path is
# broken on some platforms. If ESPEAK_LIB / ESPEAK_DATA are set (the workflow
# sets them after `apt install espeak-ng`), use the system copy instead.
if os.environ.get("ESPEAK_LIB"):
    import espeakng_loader
    espeakng_loader.get_library_path = lambda: os.environ["ESPEAK_LIB"]
    espeakng_loader.get_data_path = lambda: os.environ["ESPEAK_DATA"]

from digest import markdown_to_speech_text  # reuse the markdown→spoken cleanup

VOICE = os.environ.get("KOKORO_VOICE", "bm_george")  # "b…" = British English
_pipeline = None


def make_mp3(text, out_mp3):
    global _pipeline
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    if _pipeline is None:  # load the model once per run, not once per episode
        _pipeline = KPipeline(lang_code=VOICE[0], repo_id="hexgrad/Kokoro-82M")

    os.makedirs(os.path.dirname(out_mp3) or ".", exist_ok=True)
    speech = markdown_to_speech_text(text)
    audio = np.concatenate(
        [a for _, _, a in _pipeline(speech, voice=VOICE, split_pattern=r"\n+")]
    )

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav = tmp.name
    sf.write(wav, audio, 24000)
    # Compress to a small mono MP3 (plenty for speech).
    subprocess.run(
        ["ffmpeg", "-y", "-i", wav, "-ac", "1", "-b:a", "64k", out_mp3],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.remove(wav)
    return out_mp3


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        print(make_mp3(f.read(), sys.argv[2]))
