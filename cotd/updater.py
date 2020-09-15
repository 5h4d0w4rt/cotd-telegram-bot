import telegram
import telegram.ext
import logging
import argparse
import typing
from dataclasses import dataclass


@dataclass
class EnvConfig:
    token: str


@dataclass
class Config:
    env: EnvConfig
    updater: telegram.ext.Updater
    logger: logging.Logger
    features: typing.Optional[argparse.Namespace] = None
    options: typing.Optional[argparse.Namespace] = None


@dataclass
class COTDBotMetadata:
    me: telegram.User
    sticker_set: telegram.StickerSet
    sticker_set_file_ids: typing.List[str]


class COTDBot:

    def __init__(self, config: Config):
        self.config = config
        self.logger = self.config.logger
        self.updater = self.config.updater
        self.__me = self._fetch_user_metadata()
        self.__sticker_set = self._sticker_set()
        self.metadata = COTDBotMetadata(
            me=self.__me,
            sticker_set=self.__sticker_set[0],
            sticker_set_file_ids=self.__sticker_set[1])

        self._set_loggers()

    def _sticker_set(self) -> typing.Tuple[telegram.StickerSet, typing.List[str]]:
        fileids = []
        try:
            sticker_pack: telegram.StickerSet = self.updater.bot.get_sticker_set(
                f"VC_by_{self.__me.username}")
            if sticker_pack:
                fileids.extend(list(sticker.file_id for sticker in sticker_pack.stickers))
        except telegram.error.BadRequest as err:
            if 'Stickerset_invalid' in str(err):
                sticker_pack: telegram.StickerSet = self.updater.bot.create_new_sticker_set(
                    png_sticker=open("static/smileyOne512x512.png", 'rb'),
                    name=f"VC_by_{self.__me.username}",
                    title=f"VC_by_{self.__me.username}",
                    user_id=int(145043750),
                    emojis="🙂😊")
                fileids.extend(list(sticker.file_id for sticker in sticker_pack.stickers))
            else:
                raise
        return sticker_pack, fileids

    def _fetch_user_metadata(self):
        return self.updater.bot.get_me()

    def _set_loggers(self):
        self.logger.setLevel(self.config.options.log_level)
        self.updater.dispatcher.logger.setLevel(self.config.options.log_level)
        self.updater.dispatcher.logger.addHandler(logging.StreamHandler())
        self.updater.logger.setLevel(self.config.options.log_level)
        self.updater.logger.addHandler(logging.StreamHandler())