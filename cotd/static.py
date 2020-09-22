from dataclasses import dataclass
import typing
from types import MappingProxyType


@dataclass
class Static:
    kekw: typing.BinaryIO
    oldfellow: typing.BinaryIO
    sniff_dog: typing.BinaryIO
    ribnikov: typing.BinaryIO
    go_away: typing.BinaryIO
    ozon_secret: str


STATIC = Static(
    **MappingProxyType(
        {
            "kekw": open("static/KEKW.mp4", "rb"),
            "oldfellow": open("static/oldfellow.mp4", "rb"),
            "ribnikov": open("static/ribnikov.based.mp4", "rb"),
            "ozon_secret": "bit.ly/2Ro39uJ",
            "sniff_dog": open("static/cringe-sniff-dog.jpg", "rb"),
            "go_away": open("static/go_away.mp4", "rb"),
        }
    )
)
