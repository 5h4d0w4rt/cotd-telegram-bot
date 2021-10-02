import abc
from abc import ABCMeta
import typing
import json


class Storage(metaclass=ABCMeta):
    def __init__(self):
        raise NotImplementedError


class TelegramSavedMessagesStorage(Storage):
    def __init__(self):
        ...