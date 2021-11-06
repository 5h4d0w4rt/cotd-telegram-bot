import abc
import operator
import pathlib
import typing
from dataclasses import dataclass



class BaseStatic(metaclass=abc.ABCMeta):
    def __init__(self):
        raise NotImplementedError

    def __getattribute__(self, name: str) -> pathlib.Path:
        raise NotImplementedError

    def __setattr__(self, name: str, value: str) -> None:
        raise NotImplementedError

@dataclass
class Static(BaseStatic):
    def __init__(self, **kwargs):
        """make all instantiated attributes with relative-path-strings to absolute paths"""
        for meme in kwargs:
            self.__setattr__(meme, kwargs[meme])

    def __getattribute__(self, name: str) -> pathlib.Path:
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: str) -> None:
        object.__setattr__(self, name, pathlib.Path(pathlib.Path(value).resolve()))


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
