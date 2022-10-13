from key import *
from util import *

import time

import tweepy
import traceback


class TwitterManager:
    def __init__(self, key_dir="./key/key.json", user_id="@rand_bot_"):
        self.api = None

        self.last_id = "0"
        self.last_timestamp = "0"

        self.run = False

        #
        set_log_path()

        self.user_id = user_id

        self.key = Key(parse_json(key_dir), user_id)

        self.api = self.create_api()
        add_log("api_created", "TwitterManager.create_api")

        self.last_id = self.get_last_mention_id()
        add_log(f"get last id: {self.last_id}", "TwitterManager.get_last_mention_id")

        self.last_timestamp = self.get_last_timestamp()
        add_log(f"get last timestamp: {self.last_timestamp}", "TwitterManager.get_last_timestamp")

        self.emoji = parse_json("data/emoji.json")

    def create_api(self) -> tweepy.API:
        if self.key is None:
            raise Exception("key is none")

        if self.api is None:
            auth = tweepy.OAuthHandler(
                consumer_key=self.key.consumer_key,
                consumer_secret=self.key.consumer_secret
            )

            auth.set_access_token(
                key=self.key.access_token_key,
                secret=self.key.access_token_secret
            )

            return tweepy.API(auth)

    def get_emoji(self, account_id="", user_name="", screen_name=""):
        for item in self.emoji:
            if item["id"] == account_id or item["user_name"] == user_name or item["screen_name"] == screen_name:
                return item["emoji"]

        return None

    # mention
    def get_last_mention_id(self):
        with open("data/mention_id.txt", "r") as t:
            return t.read().strip()

    def set_last_mention_id(self):
        with open("data/mention_id.txt", "w") as t:
            t.write(self.last_id)
            add_log(f"save last id: {self.last_id}", "TwitterManager.set_last_id")

    def get_all_tweets(self):
        status = self.api.user_timeline(
            user_id=self.user_id,
            count=200
        )
        add_log("get all tweets", "TwitterManager.get_all_tweets")

        return status

    def delete_all_tweets(self):
        items = tweepy.Cursor(self.api.user_timeline).items()
        add_log(f"Start deleting.", "TwitterManager.delete_all_tweets")

        for status in items:
            try:
                self.api.destroy_status(status.id)
                add_log(f"Deleted {status.id}", "TwitterManager.delete_all_tweets")
            except Exception:
                traceback.print_exc()
                add_log(f"Failed to delete {status.id}", "TwitterManager.delete_all_tweets")

        add_log(f"Done.", "TwitterManager.delete_all_tweets")

    def respond_to_tweet(self):
        if self.last_id == "0":
            mentions = self.api.mentions_timeline()
        else:
            mentions = self.api.mentions_timeline(
                since_id=self.last_id
            )

        for mention in reversed(mentions):
            emoji = self.get_emoji(
                account_id=mention.user.id_str,
                user_name=mention.user.name,
                screen_name=f"@{mention.user.screen_name}"
            )

            if emoji is not None:

                origin_id = mention.in_reply_to_status_id_str
                user_name = mention.user.screen_name

                if origin_id is not None:
                    text = mention.text.replace(self.user_id, f"{self.user_id} {emoji}")

                    # 타래에 잇는다
                    self.api.update_status(f"{text}", in_reply_to_status_id=origin_id)
                    add_log(f"타래에 이어서 작성: {user_name}, {text}", "TwitterManager.respond_to_tweet")
                    time.sleep(3)
                else:
                    text = mention.text.replace(self.user_id, f"{emoji}")

                    # 타래를 생성
                    self.api.update_status(f"{text}")
                    add_log(f"새로운 타래를 생성: {user_name}, {text}", "TwitterManager.respond_to_tweet")
                    time.sleep(3)
            else:
                add_log(f"등록되지 않은 사용자: {mention.user.screen_name}", "TwitterManager.respond_to_tweet")

            self.last_id = mention.id_str
            self.set_last_mention_id()

    # dm
    def get_last_timestamp(self):
        with open("data/dm_timestamp.txt", "r") as t:
            return t.read().strip()

    def set_last_timestamp(self):
        with open("data/dm_timestamp.txt", "w") as t:
            t.write(self.last_timestamp)
            add_log(f"save last timestamp: {self.last_timestamp}", "TwitterManager.set_last_timestamp")

    def respond_to_direct_message(self):
        dms = self.api.get_direct_messages()

        for dm in reversed(dms):
            timestamp = dm.created_timestamp
            if timestamp > self.last_timestamp:
                # 본인이 보낸 dm은 고려하지 않음
                if dm.message_create["sender_id"] == "1402874491580030979":
                    continue

                message = dm.message_create["message_data"]["text"]

                # 보낸 사람에게 답장
                recipient_id = dm.message_create["sender_id"]

                self.api.send_direct_message(
                    recipient_id=recipient_id,
                    text="확인되었습니다",
                )
                time.sleep(0.2)
                self.api.update_status(f"{message}")
                add_log(f"dm > mention : {message}, {timestamp}", "TwitterManager.check_direct_message")
                time.sleep(2.8)

                self.last_timestamp = timestamp
                self.set_last_timestamp()

    def run(self):
        self.run = True
        while self.run:
            self.respond_to_tweet()
            time.sleep(2)
            self.respond_to_direct_message()
            time.sleep(5)

    def stop(self):
        self.run = False
