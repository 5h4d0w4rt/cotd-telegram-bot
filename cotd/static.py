from dataclasses import dataclass
import typing
from types import MappingProxyType


@dataclass
class Static:
    kekw: typing.Union[typing.BinaryIO, str]
    oldfellow: typing.Union[typing.BinaryIO, str]
    sniff_dog: typing.Union[typing.BinaryIO, str]
    stuffy: typing.Union[typing.BinaryIO, str]
    journalism: typing.Union[typing.BinaryIO, str]
    ribnikov: typing.Union[typing.BinaryIO, str]
    go_away: typing.Union[typing.BinaryIO, str]
    ozon_secret: str


def initialize_static():
    # function for automated static holder initialization, will expect a list of static files and will return static value object
    raise NotImplementedError


STATIC = Static(
    **MappingProxyType(
        {
            "kekw": open("static/KEKW.mp4", "rb"),
            "oldfellow": open("static/oldfellow.mp4", "rb"),
            "ribnikov": open("static/ribnikov.based.mp4", "rb"),
            "ozon_secret": "bit.ly/2Ro39uJ",
            "sniff_dog": open("static/cringe-sniff-dog.jpg", "rb"),
            "stuffy": open("static/stuffy.jpg", "rb"),
            "journalism": open("static/journalism.jpg", "rb"),
            "go_away": open("static/go_away.mp4", "rb"),
        }
    )
)
