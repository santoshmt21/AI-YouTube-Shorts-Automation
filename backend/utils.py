from pathlib import Path
import subprocess

FFMPEG = r"C:\ffmpeg\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\ffmpeg\ffmpeg-8.1.2-full_build\bin\ffprobe.exe"

FPS = 25
WIDTH = 1080
HEIGHT = 1920


def get_audio_duration(audio):
    result = subprocess.run(
        [
            FFPROBE,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio)
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return float(result.stdout.strip())