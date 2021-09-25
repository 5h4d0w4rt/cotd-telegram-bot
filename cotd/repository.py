import abc
from abc import ABCMeta
import typing


class Repository(metaclass=ABCMeta):
    def __init__(self, db: typing.Any):
        raise NotImplementedError

    @abc.abstractclassmethod
    def save(self) -> None:
        raise NotImplementedError

    @abc.abstractclassmethod
    def load(self) -> typing.Dict:
        raise NotImplementedError


class StubRepository(Repository):
    def __init__(self, db: typing.Dict):
        self.db = {}

    def save(self) -> None:
        return None

    def load(self) -> typing.Dict:
        return self.db