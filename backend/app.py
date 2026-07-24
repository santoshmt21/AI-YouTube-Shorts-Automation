from pathlib import Path
import shutil

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse

from renderer import build_video

app = FastAPI()

# ==========================
# CONFIG
# ==========================

EXPECTED_SCENES = 8

FFMPEG = r"C:\ffmpeg\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"

BASE = Path("assets")

IMAGE_DIR = BASE / "images"
AUDIO_DIR = BASE / "audio"
VIDEO_DIR = BASE / "videos"

IMAGE_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

video_created = False


# ==========================
# UPLOAD ENDPOINT
# ==========================

@app.post("/scene")
async def upload_scene(
    scene: int = Form(...),
    image: UploadFile = File(...),
    audio: UploadFile = File(...)
):
    global video_created

    print("=" * 60)
    print(f"Scene: {scene}")
    print(f"Image: {image.filename}")
    print(f"Audio: {audio.filename}")

    image_path = IMAGE_DIR / f"scene_{scene}.jpg"
    audio_path = AUDIO_DIR / f"scene_{scene}.mp3"

    print("Saving:", image_path)
    print("Saving:", audio_path)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    images = sorted(IMAGE_DIR.glob("scene_*.jpg"))
    audios = sorted(AUDIO_DIR.glob("scene_*.mp3"))

    print(f"Images : {len(images)}/{EXPECTED_SCENES}")
    print(f"Audios : {len(audios)}/{EXPECTED_SCENES}")

    if (
        not video_created
        and len(images) == EXPECTED_SCENES
        and len(audios) == EXPECTED_SCENES
    ):
        print("\nAll scenes received!")
        build_video()
        video_created = True

    return {
        "success": True,
        "scene": scene
    }


@app.post("/render")
def render():
    final_video = build_video()

    return FileResponse(
        path=str(final_video),
        media_type="video/mp4",
        filename="final_video.mp4"
    )