import io
import json
import typing
import zlib
from collections import defaultdict

import telegram
import telegram.ext
import telegram.ext.utils.types
from telegram import user
from telegram.ext import DictPersistence
from telegram.ext.basepersistence import BasePersistence


class TelegramSavedMessagesStorage(DictPersistence):
    def __init__(self, db, *args, **kwargs):
        self._db = db
        self._data = None
        self._cache = None
        self._bot_data = None
        self._chat_data = None
        self._user_data = None
        super().__init__(*args, **kwargs)

    def flush(self) -> None:
        delimeter = "::"
        data_to_save = json.dumps(
            {
                "db_metadata": self.bot.get_chat(chat_id=self._db).to_dict(),
                "bot_metadata": self.bot.get_me().to_dict(),
                "bot_data": self.bot_data,
                "user_data": self.user_data,
                "chat_data": self.chat_data,
            }
        )

        with io.StringIO(data_to_save) as f:
            doc = self.bot.send_document(
                chat_id=self._db, document=f, filename=f"{self.bot.username}_db.json"
            )

        self.bot.set_chat_description(
            chat_id=self._db, description=f"{self.bot.id}{delimeter}{doc.document.file_id}"
        )

    def cache(self, data):
        if not self._cache:
            self._cache = data
        return self._cache

    def _extract_bot_data_from_db(self, loaded_bot_data):
        out = defaultdict(dict)
        for top_level_key in loaded_bot_data:
            proper_top_level_key = int(top_level_key)
            for nested_key in loaded_bot_data[top_level_key]:
                proper_nested_level_key = int(nested_key)
                out[proper_top_level_key][proper_nested_level_key] = loaded_bot_data[top_level_key][
                    nested_key
                ]
        return out

    def _load(self):
        """load file from file_id that is stored in the description as bot_id::file_id string"""
        default_out = {
            "user_data": None,
            "chat_data": None,
            "bot_data": None,
        }

        try:
            _, file_id = self.bot.get_chat(self._db).description.split("::")
        except AttributeError as err:
            print("Description was not set")
            return default_out
        try:
            out = json.loads(self.bot.get_file(file_id).download_as_bytearray())
        except telegram.error.BadRequest as err:
            if err.message == "Invalid file_id":
                return default_out
        else:
            return out

    def load(self):
        return self.cache(self._load())

    def get_user_data(self):
        """"""
        res = self.load()["user_data"]
        if not res:
            return super().get_user_data()
        self._user_data = self._extract_bot_data_from_db(res)
        return self._user_data

    def get_bot_data(self):
        """"""
        res = self.load()["bot_data"]
        if not res:
            return super().get_bot_data()
        self._bot_data = self._extract_bot_data_from_db(res)
        return self._bot_data

    def get_chat_data(self):
        """"""
        res = self.load()["chat_data"]
        if not res:
            return super().get_chat_data()
        self._chat_data = self._extract_bot_data_from_db(res)
        return self._chat_data

    def update_user_data(self, user_id: int, data: typing.Dict) -> None:
        super().update_user_data(user_id, data)

    def update_bot_data(self, data: typing.Dict) -> None:
        super().update_bot_data(data)

    def update_chat_data(self, chat_id: int, data: typing.Dict) -> None:
        super().update_chat_data(chat_id, data)

    def refresh_bot_data(self, bot_data: typing.Dict) -> None:
        return super().refresh_bot_data(bot_data)

    def refresh_chat_data(self, chat_id: int, chat_data: typing.Dict) -> None:
        return super().refresh_chat_data(chat_id, chat_data)

    def refresh_user_data(self, user_id: int, user_data: typing.Dict) -> None:
        return super().refresh_user_data(user_id, user_data)


class TelegramSavedMessagesStorageDev(DictPersistence):
    def __init__(self, db, *args, **kwargs):
        self._db = db
        super().__init__(*args, **kwargs)

    def flush(self) -> None:
        ...
