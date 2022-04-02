import random
import datetime

def check_chance(percent: float = 0.5):
    return round(random.random(), 1) < percent


def check_timer(now: datetime.datetime, timer: datetime.datetime, threshold: int):
    return (now - timer).total_seconds() < threshold
