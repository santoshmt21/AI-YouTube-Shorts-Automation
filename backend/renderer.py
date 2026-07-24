import random
from pathlib import Path
import subprocess

from subtitles import generate_srt
from utils import FFMPEG, FPS, WIDTH, HEIGHT, get_audio_duration

EXPECTED_SCENES = 8

BASE = Path("assets")

IMAGE_DIR = BASE / "images"
AUDIO_DIR = BASE / "audio"
VIDEO_DIR = BASE / "videos"

VIDEO_DIR.mkdir(parents=True, exist_ok=True)
(BASE / "subtitles").mkdir(parents=True, exist_ok=True)


def create_scene_video(scene_number: int):

    image = IMAGE_DIR / f"scene_{scene_number}.jpg"
    audio = AUDIO_DIR / f"scene_{scene_number}.mp3"
    music = BASE / "music" / "background.mp3"

    output = VIDEO_DIR / f"scene_{scene_number}.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)

    duration = get_audio_duration(audio)
    frames = max(int(duration * FPS), 1)

    pan = random.choice([
        "left",
        "right",
        "up",
        "down",
        "center"
    ])

    if pan == "left":
        x = "0"
        y = "ih/2-(ih/zoom/2)"

    elif pan == "right":
        x = "iw-iw/zoom"
        y = "ih/2-(ih/zoom/2)"

    elif pan == "up":
        x = "iw/2-(iw/zoom/2)"
        y = "0"

    elif pan == "down":
        x = "iw/2-(iw/zoom/2)"
        y = "ih-ih/zoom"

    else:
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)"

    fade_out = max(duration - 1, 0)

    subtitle_file = (
        BASE /
        "subtitles" /
        "subtitles.srt"
    )

    video_filters = (
        f"scale=2500:-1,"
        f"zoompan="
        f"z='min(zoom+0.0008,1.18)':"
        f"d={frames}:"
        f"x='{x}':"
        f"y='{y}',"
        f"fps={FPS},"
        f"eq=contrast=1.08:brightness=0.03:saturation=1.15,"
        f"unsharp=5:5:1.0:5:5:0.0,"
        f"fade=t=in:st=0:d=0.7,"
        f"fade=t=out:st={fade_out}:d=0.8"
    )

    vf_filter = video_filters
    if subtitle_file.exists() and subtitle_file.stat().st_size > 0:
        vf_filter = (
            vf_filter
            + ",subtitles="
            + str(subtitle_file).replace("\\", "/")
            + ":force_style='"
            "Fontsize=18,"
            "PrimaryColour=&HFFFFFF&,"
            "OutlineColour=&H000000&,"
            "BorderStyle=1,"
            "Outline=2,"
            "Shadow=1,"
            "Alignment=2,"
            "MarginV=60"
            "'"
        )

    cmd = [
        FFMPEG,
        "-y",

        "-loop", "1",
        "-i", str(image),

        "-i", str(audio),

        "-stream_loop", "-1",
        "-i", str(music),

        "-filter_complex",

        "[1:a]volume=1.0[voice];"
        "[2:a]volume=0.12[music];"
        "[voice][music]amix=inputs=2:duration=first[a]",

        "-vf",
        vf_filter,

        "-map", "0:v",

        "-map", "[a]",

        "-c:v", "libx264",

        "-preset", "slow",

        "-crf", "17",

        "-c:a", "aac",

        "-b:a", "192k",

        "-pix_fmt", "yuv420p",

        "-movflags", "+faststart",

        "-shortest",

        str(output)
    ]

    subprocess.run(cmd, check=True)

    return output


def concat_videos(video_files):

    concat = VIDEO_DIR / "concat.txt"

    with open(concat, "w", encoding="utf8") as f:
        for video in video_files:
            f.write(f"file '{video.name}'\n")

    final_video = VIDEO_DIR / "final_video.mp4"

    cmd = [
        FFMPEG,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat),
        "-c", "copy",
        str(final_video)
    ]

    subprocess.run(cmd, check=True)

    return final_video


def build_video():

    print("\n==============================")
    print("STARTING VIDEO RENDER")
    print("==============================\n")

    generate_srt()

    videos = []

    for scene in range(1, EXPECTED_SCENES + 1):
        videos.append(create_scene_video(scene))

    final_video = concat_videos(videos)

    print("\n==============================")
    print("VIDEO CREATED SUCCESSFULLY")
    print(final_video.resolve())
    print("==============================\n")

    return final_video