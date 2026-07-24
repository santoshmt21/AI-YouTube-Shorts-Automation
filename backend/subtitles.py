import json
from pathlib import Path

from utils import get_audio_duration

BASE = Path("assets")

AUDIO = BASE / "audio"
SUBTITLE_DIR = BASE / "subtitles"

SUBTITLE_DIR.mkdir(parents=True, exist_ok=True)


def format_time(seconds):

    h = int(seconds // 3600)

    m = int((seconds % 3600) // 60)

    s = int(seconds % 60)

    ms = int((seconds-int(seconds))*1000)

    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def generate_srt():

    script = json.loads(
        Path("assets/script.json").read_text(encoding="utf8")
    )

    outfile = SUBTITLE_DIR / "subtitles.srt"
    scenes = script.get("scenes", [])

    if not scenes:
        if outfile.exists():
            outfile.unlink()
        return None

    current = 0

    with open(outfile, "w", encoding="utf8") as f:

        for i, scene in enumerate(scenes, start=1):

            audio = AUDIO / f"scene_{i}.mp3"

            duration = get_audio_duration(audio)

            start = current

            end = current + duration

            f.write(f"{i}\n")

            f.write(
                f"{format_time(start)} --> {format_time(end)}\n"
            )

            text = scene.get("voiceover", "").upper()

            f.write(text + "\n\n")

            current = end

    return outfile