from datetime import datetime
import logging
from logging import Logger
import os
from typing import Dict, List


from TwitterAPIv2 import Tweet
from TwitterAPIv2 import Media
from TwitterAPIv2.TwitterAPI import TwitterAPI


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

    tweet: Tweet.Tweet = client.get_tweet(SAMPLE_TWEET['id'], tweet_fields=SAMPLE_TWEET_FIELDS)

    assert SAMPLE_TWEET['id'] == tweet.tweet_id, 'Tweet ID が違います'
    assert SAMPLE_TWEET['text'] == tweet.text, 'Text が違います'

    assert SAMPLE_TWEET['author_id'] == tweet.author_id, 'User ID が違います'
    assert SAMPLE_TWEET['source'] == tweet.source, 'source が違います'
    assert SAMPLE_TWEET['possibly_sensitive'] == tweet.possibly_sensitive, 'possibly_sensitive が違います'
    assert SAMPLE_TWEET['lang'] == tweet.lang, '言語が違います'
    assert datetime.fromisoformat(SAMPLE_TWEET['created_at']) == tweet.created_at, 'created_at が違います'

    logger.info('[OK]normal tweet')


def test_metrics(client: TwitterAPI) -> None:

    tweet: Tweet.Tweet = client.get_tweet('1204084171334832128', tweet_fields=[Tweet.Field.PUBLIC_METRICS])

    assert tweet.public_metrics, 'public_metric を取得できていません'
    logger.debug(f'Retweet count is {tweet.public_metrics.retweet_count}')
    logger.debug(f'Quote Retweet count is {tweet.public_metrics.quote_count}')
    logger.debug(f'Like count is {tweet.public_metrics.like_count}')
    logger.debug(f'Reply count is {tweet.public_metrics.reply_count}')

    logger.info('[OK]public_metric of normal tweet')


def test_media(client: TwitterAPI) -> None:
    SAMPLE_TWEET: Dict = {
        'id': '1263145271946551300',
        'media_key': '13_1263145212760805376',
        'width': 1920,
        'height': 1080,
        'duration_ms': 46947,
        'view_count': 1845,
        'preview_image_url': 'https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg',
        'type': Media.Type.VIDEO
    }

    MEDIA_FIELDS: List[Media.Field] = [
        Media.Field.HEIGHT,
        Media.Field.WIDTH,
        Media.Field.VIEW_COUNT,
        Media.Field.DURATION_MS,
        Media.Field.PREVIEW_IMAGE_URL,
    ]

    tweet: Tweet.Tweet = client.get_tweet(SAMPLE_TWEET['id'], expansions=[Tweet.Expantion.MEDIA_KEYS], media_fields=MEDIA_FIELDS)

    assert tweet, 'Tweet が取得できません。'
    assert tweet.medias, 'Media 情報が取得できません。'
    media: Media.Media = tweet.medias[0]

    assert media.media_key == SAMPLE_TWEET['media_key']
    logger.debug(f'Media key: {media.media_key}')

    assert (width := media.width) == SAMPLE_TWEET['width'] and (height := media.height) == SAMPLE_TWEET['height'], 'サイズ情報が正しくありません。'
    logger.debug(f'Size(w*h): {width}*{height}')

    assert media.duration_ms == SAMPLE_TWEET['duration_ms'], 'duration_ms が正しくありません。'
    logger.debug(f'duration_ms: {media.duration_ms}')

    assert media.view_count, 'view_count が取得できていません。'
    logger.debug(f'View count: {media.view_count}')

    assert media.type == SAMPLE_TWEET['type'], 'メディアタイプが video ではありません。'
    logger.debug(f'Media Type: {media.type}')

    logger.info('[OK] Media Object')


def main():
    twitter: TwitterAPI = TwitterAPI(BEARER_TOKEN)

    test_normal_tweet(twitter)
    test_metrics(twitter)
    test_media(twitter)


if __name__ == "__main__":
    main()
