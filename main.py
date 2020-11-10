import os


from twitter_api_v2 import TwitterAPI
from twitter_api_v2 import Tweet


BEARER_TOKEN: str = os.environ['TWITTER_BEARER_TOKEN']


def main():
    twitter: TwitterAPI.TwitterAPI = TwitterAPI.TwitterAPI(BEARER_TOKEN)

    tweet: Tweet.Tweet = twitter.get_tweet('1326181638313664512')

    print(tweet.text)


if __name__ == "__main__":
    main()
