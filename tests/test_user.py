import os
from datetime import datetime
from typing import Dict, List

import pytest

from twitter_api_v2 import TwitterAPI, User


@pytest.fixture
def client() -> TwitterAPI.TwitterAPI:
    return TwitterAPI.TwitterAPI(os.environ["TWITTER_BEARER_TOKEN"])


def test_minimum_user(client: TwitterAPI.TwitterAPI) -> None:

    SAMPLE_USER: Dict = {
        "id": "2244994945",
        "name": "Twitter Dev",
        "username": "TwitterDev",
    }

    user: User.User = client.get_user(SAMPLE_USER["id"])

    assert user.id == SAMPLE_USER["id"], "User ID is wrong."
    assert user.name == SAMPLE_USER["name"], "name field is wrong."
    assert user.username == SAMPLE_USER["username"], "username field is wrong."


def test_not_exist_user(client: TwitterAPI.TwitterAPI) -> None:

    with pytest.raises(Exception):
        client.get_user("")


def test_normal_user(client: TwitterAPI.TwitterAPI) -> None:

    SAMPLE_USER: Dict = {
        # default fields
        "id": "2244994945",
        "name": "Twitter Dev",
        "username": "TwitterDev",
        # additional fields
        "created_at": "2013-12-14T04:35:55.000+00:00",
        "description": "The voice of the #TwitterDev team and your official source for updates, news, and events, related to the #TwitterAPI.",
        "location": "127.0.0.1",
        "url": "https://t.co/3ZX3TNiZCY",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1283786620521652229/lEODkLTh_normal.jpg",
        "protected": False,
        "pinned_tweet_id": "1293593516040269825",
        "verified": True,
    }

    SAMPLE_USER_FIELDS: List[User.Field] = [
        User.Field.CREATED_AT,
        User.Field.DESCRIPTION,
        User.Field.LOCATION,
        User.Field.PINNED_TWEET_ID,
        User.Field.PROFILE_IMAGE_URL,
        User.Field.PROTECTED,
        User.Field.URL,
        User.Field.VERIFIED,
    ]

    user: User.User = client.get_user(SAMPLE_USER["id"], user_fields=SAMPLE_USER_FIELDS)

    assert user.id == SAMPLE_USER["id"], "User ID is wrong."
    assert user.name == SAMPLE_USER["name"], "name field is wrong."
    assert user.username == SAMPLE_USER["username"], "username field is wrong."
    assert user.created_at == datetime.fromisoformat(
        SAMPLE_USER["created_at"]
    ), "created_at is wrong."
    assert user.description == SAMPLE_USER["description"], "description field is wrong."
    assert user.location == SAMPLE_USER["location"], "location field is wrong."
    assert (
        user.pinned_tweet_id == SAMPLE_USER["pinned_tweet_id"]
    ), "pinned_tweet_id field is wrong."
    assert (
        user.profile_image_url == SAMPLE_USER["profile_image_url"]
    ), "profile_image_url field is wrong."
    assert user.protected == SAMPLE_USER["protected"], "protected field is wrong."
    assert user.url == SAMPLE_USER["url"], "url field is wrong."
    assert user.verified == SAMPLE_USER["verified"], "verified field is wrong."
