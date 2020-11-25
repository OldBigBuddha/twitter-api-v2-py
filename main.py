import os
from typing import List

from twitter_api_v2 import Tweet, TwitterAPI, User

BEARER_TOKEN: str = os.environ["TWITTER_BEARER_TOKEN"]


def main():
    twitter: TwitterAPI.TwitterAPI = TwitterAPI.TwitterAPI(BEARER_TOKEN)

    # Lookup Tweet
    # If you'd like to know what you can specify fields,
    # Please read Tweet.Field class and Twitter API Document
    # FYI: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet#component-wrapper:~:text=.%20Use%20the%20expansion%20with%20the,additional%20fields%20to%20complete%20the%20object.
    tweet_fields: List[Tweet.Field] = [
        Tweet.Field.AUTHOR_ID,
        Tweet.Field.CREATED_AT,
        Tweet.Field.POSSIBLY_SENSITIVE,
        Tweet.Field.SOURCE,
    ]

    tweet: Tweet.Tweet = twitter.get_tweet(
        "1331553700058329088", tweet_fields=tweet_fields
    )

    print(tweet.author_id)
    print(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    print(tweet.lang)
    print(tweet.possibly_sensitive)

    # Lookup User by ID
    user_by_id: User.User = twitter.get_user_by_id("859754215748419584")
    print(user_by_id.id)
    print(user_by_id.username)

    # Lookup User by username(trim @ from username like @OldBigBuddha)
    # If you'd like to know what you can specify fields,
    # Please read User.Field class and Twitter API Document
    # FYI: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user#component-wrapper:~:text=.%20Use%20the%20expansion%20with%20the,additional%20fields%20to%20complete%20the%20object.
    user_fields: List[User.User] = [
        User.Field.DESCRIPTION,
        User.Field.LOCATION,
        User.Field.URL,
    ]

    user_by_username: User.User = twitter.get_user_by_username(
        "OldBigBuddha", user_fields=user_fields
    )
    print(user_by_username.description.text)
    print(user_by_username.url)


if __name__ == "__main__":
    main()
