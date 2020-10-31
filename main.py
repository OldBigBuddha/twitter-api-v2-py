import os

from TwitterAPIv2.TwitterAPI import TwitterAPI, Tweet

from datetime import datetime


BEARER_TOKEN: str = os.environ['TWITTER_BEARER_TOKEN']

TWEET_ID: str = '1212092628029698048'
SAMPLE_TWEET: dict = {
    "lang": "en",
    "id": "1212092628029698048",
    "created_at": "2019-12-31T19:26:16.000+00:00",
    "possibly_sensitive": False,
    "text": "We believe the best future version of our API will come from building it with YOU. Here\u2019s to another great year with everyone who builds on the Twitter platform. We can\u2019t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
    "author_id": "2244994945",
    "source": "Twitter Web App"
}


def main():
    twitter: TwitterAPI = TwitterAPI(BEARER_TOKEN)

    tweet: Tweet = twitter.get_tweet(TWEET_ID)
    assert SAMPLE_TWEET['id'] == tweet.tweet_id, 'Tweet ID が違います'
    assert SAMPLE_TWEET['text'] == tweet.text, 'Text が違います'
    assert SAMPLE_TWEET['author_id'] == tweet.author_id, 'User ID が違います'
    assert SAMPLE_TWEET['source'] == tweet.source, 'source が違います'
    assert SAMPLE_TWEET['possibly_sensitive'] == tweet.possibly_sensitive, 'possibly_sensitive が違います'
    assert SAMPLE_TWEET['lang'] == tweet.lang, '言語が違います'
    assert datetime.fromisoformat(SAMPLE_TWEET['created_at']) == tweet.created_at, 'created_at が違います'
    print('Assertion finished.')


if __name__ == "__main__":
    main()
