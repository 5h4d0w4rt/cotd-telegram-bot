import random
import datetime


def check_chance(percent: float = 0.5):
    return round(random.random(), 1) < percent


def check_timer(now: datetime.datetime, timer: datetime.datetime, threshold: int):
    return (now - timer).total_seconds() < threshold


def webm_to_mp4():
    import subprocess

    out = subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc2=d=1[out0];sine=d=1[out1]", "test.mp4"]
    )
    return out.returncode
