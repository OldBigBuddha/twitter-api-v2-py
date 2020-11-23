from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from twitter_api_v2.Metric import Metric
from twitter_api_v2.util import get_additional_field


class Field(Enum):

    CREATED_AT: str = "created_at"
    DESCRIPTION: str = "description"
    ENTITIES: str = "entities"
    LOCATION: str = "location"
    PINNED_TWEET_ID: str = "pinned_tweet_id"
    PROFILE_IMAGE_URL: str = "profile_image_url"
    PROTECTED: str = "protected"
    PUBLIC_METRICS: str = "public_metrics"
    URL: str = "url"
    VERIFIED: str = "verified"
    WITHHELD: str = "withheld"

    def __str__(self) -> str:
        return self.value


class PublicMetric(Metric):
    def __init__(self, data: Dict[str, int]) -> None:
        self.followers_count: int = data["followers_count"]
        self.following_count: int = data["following_count"]
        self.tweet_count: int = data["tweet_count"]
        self.listed_count: int = data["listed_count"]


class User:
    def __init__(self, id: str, name: str, username: str, *args, **kwargs) -> None:
        self.id: str = id
        self.name: str = name
        self.username: str = username

        # Additional field
        self.created_at: Optional[datetime] = None
        if (created_at := get_additional_field(kwargs, "created_at")) is not None:
            self.created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        self.description: Optional[str] = get_additional_field(kwargs, "description")

        # TODO: Implement Entity object
        self.entities: Optional[Dict] = None

        self.location: Optional[str] = get_additional_field(kwargs, "location")
        self.pinned_tweet_id: Optional[str] = get_additional_field(
            kwargs, "pinned_tweet_id"
        )
        self.profile_image_url: Optional[str] = get_additional_field(
            kwargs, "profile_image_url"
        )
        self.protected: Optional[bool] = get_additional_field(kwargs, "protected", bool)
        self.public_metrics: Optional[PublicMetric] = get_additional_field(
            kwargs, "public_metrics", PublicMetric
        )
        self.url: Optional[str] = get_additional_field(kwargs, "url")
        self.verified: Optional[bool] = get_additional_field(kwargs, "verified")

        # TODO: Check https://help.twitter.com/en/rules-and-policies/tweet-withheld-by-country
        self.withheld: Optional[Dict] = None
