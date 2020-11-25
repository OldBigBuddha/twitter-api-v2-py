from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from twitter_api_v2 import Entity
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


class Description:
    def __init__(
        self,
        text: str = "",
    ) -> None:

        self.text: str = text

        self.cashtags: Optional[List[Entity.CashTag]] = None
        self.hashtags: Optional[List[Entity.HashTag]] = None
        self.mentions: Optional[List[Entity.Mention]] = None
        self.urls: Optional[List[Entity.Url]] = None


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

        self.description: Optional[Description] = None
        if (text := get_additional_field(kwargs, "description")) :
            description: Description = Description(text)

            if (
                "entities" in kwargs.keys()
                and "description" in kwargs["entities"].keys()
            ):
                description_res: Dict = kwargs["entities"]["description"]

                if "cashtags" in description_res.keys():
                    cashtags: List[Dict] = description_res["cashtags"]
                    description.cashtags = []
                    for cashtag in cashtags:
                        description.cashtags.append(
                            Entity.CashTag(
                                cashtag["start"], cashtag["end"], cashtag["tag"]
                            )
                        )

                if "hashtags" in description_res.keys():
                    hashtags: List[Dict] = description_res["hashtags"]
                    description.hashtags = []
                    for hashtag in hashtags:
                        description.hashtags.append(
                            Entity.HashTag(
                                hashtag["start"], hashtag["end"], hashtag["tag"]
                            )
                        )

                if "mentions" in description_res.keys():
                    mentions: List[Dict] = description_res["mentions"]
                    description.mentions = []
                    for mention in mentions:
                        description.mentions.append(
                            Entity.Mention(
                                mention["start"], mention["end"], mention["tag"]
                            )
                        )

                if "urls" in description_res.keys():
                    urls: List[Dict] = description_res["urls"]
                    description.urls = []
                    for url in urls:
                        description.urls.append(
                            Entity.Url(
                                url["start"],
                                url["end"],
                                url["url"],
                                url["expanded_url"],
                                url["display_url"],
                            )
                        )

            self.description = description

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

        self.url: Optional[Union[str, Entity.Url]] = get_additional_field(kwargs, "url")
        if "entities" in kwargs.keys() and "url" in kwargs["entities"].keys():
            url_res: Dict = kwargs["entities"]["url"]["urls"][0]
            self.url = Entity.Url(
                url_res["start"],
                url_res["end"],
                url_res["url"],
                url_res["expanded_url"],
                url_res["display_url"],
            )

        self.verified: Optional[bool] = get_additional_field(kwargs, "verified", bool)

        # TODO: Check https://help.twitter.com/en/rules-and-policies/tweet-withheld-by-country
        self.withheld: Optional[Dict] = None
