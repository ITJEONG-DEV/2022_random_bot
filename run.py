from twitter_manager import *

if __name__ == "__main__":
    twitter_manager = TwitterManager(
        key_dir="key/key.json",
        user_id="@rand_bot_"
    )

    twitter_manager.run()

    # twitter_manager.delete_all_tweets()

    # twitter_manager.respond_to_tweet()

    # twitter_manager.respond_to_direct_message()

