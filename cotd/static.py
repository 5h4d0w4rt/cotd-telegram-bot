from dataclasses import dataclass
import typing
from types import MappingProxyType


@dataclass
class Static:
    kekw: typing.IO
    oldfellow: typing.IO
    sniff_dog: typing.IO
    ozon_secret: str


static = MappingProxyType({
    'kekw': open('static/KEKW.mp4', 'rb'),
    'oldfellow': open("static/oldfellow.mp4", 'rb'),
    'ozon_secret': 'bit.ly/2Ro39uJ',
    'sniff_dog': open("static/cringe-sniff-dog.jpg", 'rb')
})

STATIC = Static(**static)