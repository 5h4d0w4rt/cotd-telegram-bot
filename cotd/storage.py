import io
import json
import typing
import zlib
from collections import defaultdict

import telegram
import telegram.ext
import telegram.ext.utils.types
from telegram.ext import DictPersistence
from telegram.ext.basepersistence import BasePersistence


class TelegramSavedMessagesStorage(DictPersistence):
    def __init__(self, db, *args, **kwargs):
        self._db = db
        self._data = None
        super().__init__(*args, **kwargs)

    def flush(self) -> None:

        data_to_save = json.dumps(
            {
                "db_metadata": self.bot.get_chat(chat_id=self._db).to_dict(),
                "bot_metadata": self.bot.get_me().to_dict(),
                "bot_data": self.user_data,
                "user_data": self.bot_data,
                "chat_data": self.chat_data,
            }
        )

        with io.StringIO(data_to_save) as f:
            doc = self.bot.send_document(
                chat_id=self._db, document=f, filename=f"{self.bot.username}_db.json"
            )

        self.bot.set_chat_description(
            chat_id=self._db, description=f"{self.bot.id}::{doc.document.file_id}"
        )

    def _load(self):

        if self._data:
            return self._data

        chat = self.bot.get_chat(self._db)
        file_id = chat.description.split("::")
        try:
            out = json.loads(self.bot.get_file(file_id).download_as_bytearray())
        except telegram.error.BadRequest as err:
            if err.message == "Invalid file_id":
                default_out = {
                    "user_data": None,
                    "chat_data": None,
                    "bot_data": None,
                }
                self._data = default_out
                return default_out
        else:
            self._data = out
            return out

    def load(self) -> typing.Dict:
        return self._load()

    def get_user_data(self):
        """"""
        res = self.load()["user_data"]
        if not res:
            return super().get_user_data()
        return res

    def get_bot_data(self):
        """"""
        res = self.load()["bot_data"]
        if not res:
            return super().get_bot_data()
        return res

    def get_chat_data(self):
        """"""
        res = self.load()["chat_data"]
        if not res:
            return super().get_chat_data()
        return res


class TelegramSavedMessagesStorageDev(DictPersistence):
    def __init__(self, db, *args, **kwargs):
        self._db = db
        super().__init__(*args, **kwargs)

    def flush(self) -> None:
        ...
