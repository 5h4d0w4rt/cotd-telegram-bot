import abc
from abc import ABCMeta
from typing import Dict
from telegram.ext import DictPersistence


class TelegramSavedMessagesStorage(DictPersistence):
    def __init__(self):
        super().__init__()
