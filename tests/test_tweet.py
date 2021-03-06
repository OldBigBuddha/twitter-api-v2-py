import os
from datetime import datetime
from typing import Dict, List

import pytest

from twitter_api_v2 import Media, Poll, Tweet, TwitterAPI


@pytest.fixture
def client() -> TwitterAPI.TwitterAPI:
    return TwitterAPI.TwitterAPI(os.environ["TWITTER_BEARER_TOKEN"])


def test_minimum_tweet(client: TwitterAPI.TwitterAPI) -> None:

    SAMPLE_TWEET: Dict = {
        "id": "1212092628029698048",
        "text": "We believe the best future version of our API will come from building it with YOU. Here\u2019s to another great year with everyone who builds on the Twitter platform. We can\u2019t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
    }

    tweet: Tweet.Tweet = client.get_tweet(SAMPLE_TWEET["id"])

    assert tweet.text == SAMPLE_TWEET["text"], "text field is wrong."


def test_not_exist_tweet(client: TwitterAPI.TwitterAPI) -> None:
    with pytest.raises(Exception):
        client.get_tweet("")


def test_normal_tweet(client: TwitterAPI.TwitterAPI) -> None:

    SAMPLE_TWEET: Dict = {
        # default fields
        "id": "1212092628029698048",
        "text": "We believe the best future version of our API will come from building it with YOU. Here\u2019s to another great year with everyone who builds on the Twitter platform. We can\u2019t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
        # additional fields
        "author_id": "2244994945",
        "created_at": "2019-12-31T19:26:16.000+00:00",
        "lang": "en",
        "possibly_sensitive": False,
        "source": "Twitter Web App",
    }

    SAMPLE_TWEET_FIELDS: List[Tweet.Field] = [
        Tweet.Field.AUTHOR_ID,
        Tweet.Field.CREATED_AT,
        Tweet.Field.LANG,
        Tweet.Field.POSSIBLY_SENSITIVE,
        Tweet.Field.SOURCE,
    ]

    tweet: Tweet.Tweet = client.get_tweet(
        SAMPLE_TWEET["id"], tweet_fields=SAMPLE_TWEET_FIELDS
    )

    assert SAMPLE_TWEET["id"] == tweet.id, "Tweet ID is wrong."
    assert SAMPLE_TWEET["text"] == tweet.text, "text is wrong."

    assert SAMPLE_TWEET["author_id"] == tweet.author_id, "User ID is wrong."
    assert SAMPLE_TWEET["source"] == tweet.source, "source is wrong."
    assert (
        SAMPLE_TWEET["possibly_sensitive"] == tweet.possibly_sensitive
    ), "possibly_sensitive is wrong."
    assert SAMPLE_TWEET["lang"] == tweet.lang, "lang is wrong."
    assert (
        datetime.fromisoformat(SAMPLE_TWEET["created_at"]) == tweet.created_at
    ), "created_at is wrong."


def test_metrics_object(client: TwitterAPI.TwitterAPI) -> None:

    tweet: Tweet.Tweet = client.get_tweet(
        "1204084171334832128", tweet_fields=[Tweet.Field.PUBLIC_METRICS]
    )

    assert tweet.public_metrics, "public_metric should exist."
    assert tweet.public_metrics.retweet_count, "public_metric should exist."
    assert tweet.public_metrics.quote_count, "quote_count should exist."
    assert tweet.public_metrics.like_count, "like_count should exist."
    assert tweet.public_metrics.reply_count, "reply_count should exist."


def test_media_object(client: TwitterAPI.TwitterAPI) -> None:
    SAMPLE_TWEET: Dict = {
        "id": "1263145271946551300",
        "media_key": "13_1263145212760805376",
        "width": 1920,
        "height": 1080,
        "duration_ms": 46947,
        "view_count": 1845,
        "preview_image_url": "https://pbs.twimg.com/media/EYeX7akWsAIP1_1.jpg",
        "type": Media.Type.VIDEO,
    }

    MEDIA_FIELDS: List[Media.Field] = [
        Media.Field.HEIGHT,
        Media.Field.WIDTH,
        Media.Field.VIEW_COUNT,
        Media.Field.DURATION_MS,
        Media.Field.PREVIEW_IMAGE_URL,
    ]

    tweet: Tweet.Tweet = client.get_tweet(
        SAMPLE_TWEET["id"],
        expansions=[Tweet.Expantion.MEDIA_KEYS],
        media_fields=MEDIA_FIELDS,
    )

    assert tweet.medias, "media should exist."
    media: Media.Media = tweet.medias[0]

    assert media.media_key == SAMPLE_TWEET["media_key"], "media_key is wrong."
    assert media.width == SAMPLE_TWEET["width"], "width is wrong"
    assert media.height == SAMPLE_TWEET["height"], "height is wrong."
    assert media.duration_ms == SAMPLE_TWEET["duration_ms"], "duration_ms is wrong."
    assert media.view_count, "view_count should exist."
    assert media.type == SAMPLE_TWEET["type"], "type should be video."


def test_poll_object(client: TwitterAPI.TwitterAPI) -> None:

    SAMPLE_TWEET: Dict = {
        "id": "1199786642791452673",
        "options": [
            {"label": "“C Sharp”", "votes": 795},
            {"label": "“C Hashtag”", "votes": 156},
        ],
        "status": Poll.Status.CLOSED,
        "duration_minutes": 1440,
        "end_datetime": datetime.fromisoformat("2019-11-28T20:26:41.000+00:00"),
    }

    POLL_FIELDS: List[Poll.Field] = [
        Poll.Field.DURATION_MINUTES,
        Poll.Field.END_DATETIME,
        Poll.Field.VOTING_STATUS,
    ]

    tweet: Tweet.Tweet = client.get_tweet(
        SAMPLE_TWEET["id"], [Tweet.Expantion.POLL_IDS], poll_fields=POLL_FIELDS
    )

    assert tweet, "Tweet should exist."
    assert tweet.polls, "Poll should exist."

    for poll in tweet.polls:
        assert poll.id, "Poll ID should exist."

        assert poll.options, "Options should exist."
        for idx, option in enumerate(poll.options):
            assert option.position == idx + 1, "position is wrong."
            assert (
                option.label == SAMPLE_TWEET["options"][idx]["label"]
            ), "label is wrong."
            assert (
                option.votes == SAMPLE_TWEET["options"][idx]["votes"]
            ), "votes is wrong."

        assert (
            poll.duration_minutes == SAMPLE_TWEET["duration_minutes"]
        ), "duration_minutes is wrong."
        assert poll.end_datetime == SAMPLE_TWEET["end_datetime"], "datetime is wrong."
        assert poll.voting_status == SAMPLE_TWEET["status"], "voting_status is wrong."


def test_entities_for_tweet(client: TwitterAPI.TwitterAPI) -> None:
    SAMPLE_TWEET: Dict = {
        # default fields
        "id": "1212092628029698048",
        "text": "We believe the best future version of our API will come from building it with YOU. Here\u2019s to another great year with everyone who builds on the Twitter platform. We can\u2019t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
        "entities": {
            "annotations": [
                {
                    "start": 144,
                    "end": 150,
                    "probability": 0.626,
                    "type": "Product",
                    "normalized_text": "Twitter",
                }
            ],
            "urls": [
                {
                    "start": 222,
                    "end": 245,
                    "url": "https://t.co/yvxdK6aOo2",
                    "expanded_url": "https://twitter.com/LovesNandos/status/1211797914437259264/photo/1",
                    "display_url": "pic.twitter.com/yvxdK6aOo2",
                }
            ],
        },
    }

    tweet: Tweet.Tweet = client.get_tweet(
        SAMPLE_TWEET["id"], tweet_fields=[Tweet.Field.ENTITIES]
    )

    assert tweet.id == SAMPLE_TWEET["id"], "Tweet ID is wrong."
    assert tweet.entities, "entities should exist."

    entities: Dict = SAMPLE_TWEET["entities"]

    assert tweet.entities.annotations, "annotations should exist."
    SAMPLE_ANNOTATION: List[Dict] = entities["annotations"]
    for idx, annotation in enumerate(tweet.entities.annotations):
        assert (
            annotation.start == SAMPLE_ANNOTATION[idx]["start"]
        ), f"Annotation{idx}: start is wrong."
        assert (
            annotation.end == SAMPLE_ANNOTATION[idx]["end"]
        ), f"Annotation{idx}: end is wrong."
        assert (
            annotation.probability == SAMPLE_ANNOTATION[idx]["probability"]
        ), f"Annotation{idx}: probability is wrong."
        assert (
            annotation.type == SAMPLE_ANNOTATION[idx]["type"]
        ), f"Annotation{idx}: type is wrong."
        assert (
            annotation.normalized_text == SAMPLE_ANNOTATION[idx]["normalized_text"]
        ), f"Annotation{idx}: normalized_text is wrong."

    assert tweet.entities.urls, "urls should exist."
    SAMPLE_URLS: List[Dict] = entities["urls"]
    for idx, url in enumerate(tweet.entities.urls):
        assert url.start == SAMPLE_URLS[idx]["start"], f"URL[{idx}]: start is wrong."
        assert url.end == SAMPLE_URLS[idx]["end"], f"URL[{idx}]: end is wrong."
        assert url.url == SAMPLE_URLS[idx]["url"], f"URL[{idx}]: url is wrong."
        assert (
            url.expanded_url == SAMPLE_URLS[idx]["expanded_url"]
        ), f"URL[{idx}]: expanded_url is wrong."
        assert (
            url.display_url == SAMPLE_URLS[idx]["display_url"]
        ), f"URL[{idx}]: display_url is wrong."

    assert tweet.entities.cashtags is None, "cashtags should be None."
    assert tweet.entities.hashtags is None, "hashtags should be None."
    assert tweet.entities.mentions is None, "mentions should be None."


def test_context_annotation(client: TwitterAPI.TwitterAPI) -> None:
    SAMPLE_TWEET: Dict = {
        "id": "1212092628029698048",
        "text": "We believe the best future version of our API will come from building it with YOU. Here’s to another great year with everyone who builds on the Twitter platform. We can’t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
        "context_annotations": [
            {
                "domain": {
                    "id": "119",
                    "name": "Holiday",
                    "description": "Holidays like Christmas or Halloween",
                },
                "entity": {"id": "1186637514896920576", "name": " New Years Eve"},
            },
            {
                "domain": {
                    "id": "119",
                    "name": "Holiday",
                    "description": "Holidays like Christmas or Halloween",
                },
                "entity": {
                    "id": "1206982436287963136",
                    "name": "Happy New Year: It’s finally 2020 everywhere!",
                    "description": "Catch fireworks and other celebrations as people across the globe enter the new year.\nPhoto via @GettyImages ",
                },
            },
            {
                "domain": {
                    "id": "46",
                    "name": "Brand Category",
                    "description": "Categories within Brand Verticals that narrow down the scope of Brands",
                },
                "entity": {"id": "781974596752842752", "name": "Services"},
            },
            {
                "domain": {
                    "id": "47",
                    "name": "Brand",
                    "description": "Brands and Companies",
                },
                "entity": {"id": "10045225402", "name": "Twitter"},
            },
            {
                "domain": {
                    "id": "119",
                    "name": "Holiday",
                    "description": "Holidays like Christmas or Halloween",
                },
                "entity": {
                    "id": "1206982436287963136",
                    "name": "Happy New Year: It’s finally 2020 everywhere!",
                    "description": "Catch fireworks and other celebrations as people across the globe enter the new year.\nPhoto via @GettyImages ",
                },
            },
        ],
        "entities": {
            "annotations": [
                {
                    "start": 144,
                    "end": 150,
                    "probability": 0.626,
                    "type": "Product",
                    "normalized_text": "Twitter",
                }
            ],
            "urls": [
                {
                    "start": 222,
                    "end": 245,
                    "url": "https://t.co/yvxdK6aOo2",
                    "expanded_url": "https://twitter.com/LovesNandos/status/1211797914437259264/photo/1",
                    "display_url": "pic.twitter.com/yvxdK6aOo2",
                }
            ],
        },
    }

    tweet: Tweet.Tweet = client.get_tweet(
        SAMPLE_TWEET["id"],
        tweet_fields=[Tweet.Field.CONTEXT_ANNOTATIONS, Tweet.Field.ENTITIES],
    )

    assert tweet.id == SAMPLE_TWEET["id"], "Tweet ID is wrong."
    assert tweet.text == SAMPLE_TWEET["text"], "text is wrong."

    assert tweet.context_annotations, "context_annotations should exist."

    SAMPLE_CONTEXT_ANNOTATIONS: List[Dict] = SAMPLE_TWEET["context_annotations"]
    for idx, context_annotation in enumerate(tweet.context_annotations):
        if (domain := context_annotation[0]) :
            SAMPLE_DOMAIN: Dict = SAMPLE_CONTEXT_ANNOTATIONS[idx]["domain"]
            assert (
                domain.id == SAMPLE_DOMAIN["id"]
            ), f"context_annotation[{idx}].domain.id is wrong."
            assert (
                domain.name == SAMPLE_DOMAIN["name"]
            ), f"context_annotation[{idx}].domain.name is wrong."
            if domain.description:
                assert (
                    domain.description == SAMPLE_DOMAIN["description"]
                ), f"context_annotation[{idx}].domain.description is wrong."

        if (entity := context_annotation[1]) :
            SAMPLE_ENTITY: Dict = SAMPLE_CONTEXT_ANNOTATIONS[idx]["entity"]
            assert (
                entity.id == SAMPLE_ENTITY["id"]
            ), f"context_annotation[{idx}].domain.id is wrong."
            assert (
                entity.name == SAMPLE_ENTITY["name"]
            ), f"context_annotation[{idx}].domain.name is wrong."
            if entity.description:
                assert (
                    entity.description == SAMPLE_ENTITY["description"]
                ), f"context_annotation[{idx}].domain.description is wrong."
