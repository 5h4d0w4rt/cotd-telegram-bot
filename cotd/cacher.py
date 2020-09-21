import abc
import typing


class MediaCache(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def __getattribute__(self, name: str) -> typing.Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setattr__(self, name: str, value: typing.Any) -> None:
        raise NotImplementedError


class MediaCacheInMemory(MediaCache):
    def __init__(self):
        pass

    def __getattribute__(self, name: str) -> typing.Union[typing.Any, None]:
        try:
            result = object.__getattribute__(self, name)
        except AttributeError:
            return None
        else:
            return result

    def __setattr__(self, name: str, value: typing.Any) -> None:
        object.__setattr__(self, name, value)
