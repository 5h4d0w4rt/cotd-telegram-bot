import builtins
import gzip
import io
import json
import typing
from collections import defaultdict

import telegram
import telegram.ext
import telegram.ext.utils.types
from telegram.ext import DictPersistence
from telegram.utils.types import FileLike


class TelegramDocumentDatabaseManagerMixin:
    """This mixin class is responsible for upload/download and managing "database"(chat that bot controls)
    This is mixin expected to be mixed to storage class that will write to telegram channel as a backend
    """
    bot: telegram.Bot
    db: str
    DELIMETER = "::"

    def __init__(self) -> None:
        # this will call next class in MRO
        super().__init__()

    def _send_document(self, document: io.BytesIO | io.StringIO) -> telegram.Message:
        msg = self.bot.send_document(
                chat_id=self.db, document=document, filename=f"{self.bot.username}.db",
        )
        self.bot.edit_message_caption(
            caption=f"file_id::{msg.document.file_id}",
            message_id=msg.message_id,
            chat_id=self.db
        )
        return msg

    def download(self, file_id: str) -> bytes | None:
        try:
            out = self.bot.get_file(file_id).download_as_bytearray()
        except telegram.error.BadRequest as err:
            if err.message == "Invalid file_id":
                return None
        else:
            return out

    def store_file_id_in_description(self, file_id: str) -> bool:
        """encode uploaded file_id to description for later retrieval"""
        return self.bot.set_chat_description(
            chat_id=self.db,
            description=f"{self.bot.id}{self.DELIMETER}{file_id}"
        )

    def retrieve_file_from_description(self) -> bytes | None:
        """decode description, authenticate data and return the result"""
        try:
            bot_id, file_id = self.bot.get_chat(self.db).description.split(f"{self.DELIMETER}")
        except AttributeError:
            print("Description was not set or encoding is incorrect")
        else:
            if self.bot.id == bot_id:
                return self.download(file_id)
            else:
                # same energy lmao
                return self.download(file_id)

    def upload(self, data: str | bytes) -> telegram.Message:

        match type(data):
            case builtins.str:
                # this is to ensure pyright will recognize the type
                assert type(data) is str
                with io.StringIO(data) as f:
                    return self._send_document(f)
            case builtins.bytes:
                # this is to ensure pyright will recognize the type
                assert type(data) is bytes
                with io.BytesIO(data) as f:
                    return self._send_document(f)
            case _:
                raise ValueError("Data should be either of bytes or str type")

class TelegramSavedMessagesStorage(TelegramDocumentDatabaseManagerMixin, DictPersistence):

    def __init__(self, db):
        self._data = None
        self._cache = None
        self._bot_data = None
        self._chat_data = None
        self._user_data = None

        super().__init__()

        self.db = db

    def flush(self) -> None:

        data_to_save = gzip.compress(json.dumps(
            {
                "db_metadata": self.bot.get_chat(chat_id=self.db).to_dict(),
                "bot_metadata": self.bot.get_me().to_dict(),
                "bot_data": self.bot_data,
                "user_data": self.user_data,
                "chat_data": self.chat_data,
            }
        ).encode('utf-8'))
        document = self.upload(data_to_save)
        successfully_set_description = self.store_file_id_in_description(document.document.file_id)
        if not successfully_set_description:
            # backup for manual recovery
            self.bot.send_message(self.db, text = f"backup+{self.bot.id}+{document.document.file_id}")
            raise ValueError("Setting description failed")


    def cache(self, data: bytes | None) -> bytes | None:
        if not self._cache:
            self._cache = data
        return self._cache

    def _extract_bot_data_from_db(self, loaded_bot_data):
        out = defaultdict(dict)
        if "cache" in loaded_bot_data:
            out |= loaded_bot_data
            return out

        # make all dumped integers that became string integers again
        for top_level_key in loaded_bot_data:
            proper_top_level_key = int(top_level_key)
            out[proper_top_level_key] = {}
            for nested_key in loaded_bot_data[top_level_key]:
                proper_nested_level_key = int(nested_key)
                out[proper_top_level_key][proper_nested_level_key] = loaded_bot_data[top_level_key][
                    nested_key
                ]
        return out


    def load(self) -> dict:
        default = {
            "user_data": None,
            "chat_data": None,
            "bot_data": None,
        }

        if (res := self.cache(self.retrieve_file_from_description())) is not None:
            try:
                return json.loads(gzip.decompress(res))
            except gzip.BadGzipFile:
                return json.loads(res)

        return default

    def get_user_data(self):
        """"""
        res = self.load()
        if not res:
            default = super().get_user_data()
            return default

        self._user_data = self._extract_bot_data_from_db(res["user_data"])
        return self._user_data

    def get_bot_data(self):
        """"""
        res = self.load()
        if not res:
            default = super().get_bot_data()
            return default

        self._bot_data = self._extract_bot_data_from_db(res["bot_data"])
        return self._bot_data

    def get_chat_data(self):
        """"""
        res = self.load()
        if not res:
            default = super().get_chat_data()
            return default

        self._chat_data = self._extract_bot_data_from_db(res["chat_data"])
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


class TelegramSavedMessagesStorageDev(TelegramDocumentDatabaseManagerMixin, DictPersistence):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def flush(self) -> None:

        data_to_save = gzip.compress(json.dumps(
                {
                    "db_metadata": self.bot.get_chat(chat_id=self.db).to_dict(),
                    "bot_metadata": self.bot.get_me().to_dict(),
                    "bot_data": self.bot_data,
                    "user_data": self.user_data,
                    "chat_data": self.chat_data,
                }
            ).encode('utf-8'))
        document = self.upload(data_to_save)
        if ( d := self.download(document.document.file_id)) is not None:
            try:
                print("decompressed")
                print(json.loads(gzip.decompress(d)))
            except gzip.BadGzipFile as err:
                print('failed to decompress, loading json')
                print(json.loads(d))
