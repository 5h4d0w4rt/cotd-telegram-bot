from dataclasses import dataclass
from os import path
import typing
from types import MappingProxyType

import pathlib
import operator
import abc


@dataclass
class Static:
    files: MappingProxyType

    def __post_init__(self):
        """make all instantiated attributes with relative-path-strings to absolute paths"""
        for meme in self.files:
            object.__setattr__(self, meme, pathlib.Path(pathlib.Path(self.files[meme]).resolve()))
        del self.files


class BaseStaticReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __getattribute__(self, name: str) -> typing.BinaryIO:
        raise NotImplementedError


class StaticReader(BaseStaticReader):
    static: Static

    def __init__(self, static) -> None:
        self.static = static
        super().__init__()

    def __getattribute__(self, name: str) -> typing.BinaryIO:
        """access static holder and make it's attributes readable objects"""
        # access subattribute by making curried attrgetter function call
        path_to_file: pathlib.Path = operator.attrgetter(name)(
            object.__getattribute__(self, "static")
        )
        return open(path_to_file, "rb")


# # "ozon_secret": "bit.ly/2Ro39uJ" is forgotten here
