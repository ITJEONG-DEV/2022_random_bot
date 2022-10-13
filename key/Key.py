from util import *


class Key:
    def __init__(self, file: json, user_id: str):
        self.__consumer_key__ = file["api_key"]
        self.__consumer_secret__ = file["api_key_secret"]

        self.__bearer_token__ = file["bearer_token"]

        self.__access_token_key = ""
        self.__access_token_secret = ""

        access_data = file["access"]

        for data in access_data:
            if data["id"] == user_id:
                self.__access_token_key = data["access_token"]
                self.__access_token_secret = data["access_token_secret"]

        if self.__access_token_key == "":
            self.__access_token_key = access_data[0]["access_token"]
            self.__access_token_secret = access_data[0]["access_token_secret"]

        add_log(f"key created", "Key.__init__")

    @property
    def consumer_key(self):
        return self.__consumer_key__

    @property
    def consumer_secret(self):
        return self.__consumer_secret__

    @property
    def bearer_token(self):
        return self.__bearer_token__

    @property
    def access_token_key(self):
        return self.__access_token_key

    @property
    def access_token_secret(self):
        return self.__access_token_secret
