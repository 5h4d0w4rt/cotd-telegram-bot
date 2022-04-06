import random
import datetime
import subprocess


def check_chance(percent: float = 0.5):
    return round(random.random(), 1) < percent


def check_timer(now: datetime.datetime, timer: datetime.datetime, threshold: int):
    return (now - timer).total_seconds() < threshold


def webm_to_mp4(ins, outs):

    result = subprocess.run(["ffmpeg", "-y", "-i", ins, outs])
    return result.returncode, result.stderr
