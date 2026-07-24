from pathlib import Path

BASE_DIR = Path(__file__).parent

ASSETS = BASE_DIR / "assets"

IMAGE_DIR = ASSETS / "images"
AUDIO_DIR = ASSETS / "audio"
VIDEO_DIR = ASSETS / "videos"
OUTPUT_DIR = ASSETS / "output"

LOG_DIR = BASE_DIR / "logs"

for folder in [
    IMAGE_DIR,
    AUDIO_DIR,
    VIDEO_DIR,
    OUTPUT_DIR,
    LOG_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)