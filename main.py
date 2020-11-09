from datetime import datetime
import logging
from logging import Logger
import os
from typing import Dict, List

from TwitterAPIv2.TwitterAPI import TwitterAPI, Tweet


BEARER_TOKEN: str = os.environ['TWITTER_BEARER_TOKEN']

# logging
logging.basicConfig(level=logging.DEBUG)
logger: Logger = logging.getLogger(__name__)


def test_normal_tweet(client: TwitterAPI) -> None:

    SAMPLE_TWEET: Dict = {
        # default fields
        "id": "1212092628029698048",
        "text": "We believe the best future version of our API will come from building it with YOU. Here\u2019s to another great year with everyone who builds on the Twitter platform. We can\u2019t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",

        # additional fields
        "author_id": "2244994945",
        "created_at": "2019-12-31T19:26:16.000+00:00",
        "lang": "en",
        "possibly_sensitive": False,
        "source": "Twitter Web App"
    }

    SAMPLE_TWEET_FIELDS: List[Tweet.Field] = [
        Tweet.Field.AUTHOR_ID,
        Tweet.Field.CREATED_AT,
        Tweet.Field.LANG,
        Tweet.Field.POSSIBLY_SENSITIVE,
        Tweet.Field.SOURCE
    ]

    tweet: Tweet.Tweet = client.get_tweet(SAMPLE_TWEET['id'], SAMPLE_TWEET_FIELDS)

    assert SAMPLE_TWEET['id'] == tweet.tweet_id, 'Tweet ID が違います'
    assert SAMPLE_TWEET['text'] == tweet.text, 'Text が違います'

    assert SAMPLE_TWEET['author_id'] == tweet.author_id, 'User ID が違います'
    assert SAMPLE_TWEET['source'] == tweet.source, 'source が違います'
    assert SAMPLE_TWEET['possibly_sensitive'] == tweet.possibly_sensitive, 'possibly_sensitive が違います'
    assert SAMPLE_TWEET['lang'] == tweet.lang, '言語が違います'
    assert datetime.fromisoformat(SAMPLE_TWEET['created_at']) == tweet.created_at, 'created_at が違います'

    logger.info('[OK]normal tweet')


def test_metrics(client: TwitterAPI) -> None:

    tweet: Tweet.Tweet = client.get_tweet('1204084171334832128', [Tweet.Field.PUBLIC_METRICS])

    assert tweet.public_metrics, 'public_metric を取得できていません'
    logger.debug(f'Retweet count is {tweet.public_metrics.retweet_count}')
    logger.debug(f'Quote Retweet count is {tweet.public_metrics.quote_count}')
    logger.debug(f'Like count is {tweet.public_metrics.like_count}')
    logger.debug(f'Reply count is {tweet.public_metrics.reply_count}')

    logger.info('[OK]public_metric of normal tweet')


def main():
    twitter: TwitterAPI = TwitterAPI(BEARER_TOKEN)

    test_normal_tweet(twitter)
    test_metrics(twitter)


if __name__ == "__main__":
    main()
