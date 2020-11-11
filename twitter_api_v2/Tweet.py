from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional

from twitter_api_v2.Media import Media
from twitter_api_v2.Metric import PublicMetric
from twitter_api_v2.Poll import Poll
from twitter_api_v2.util import get_additional_field


class Field(Enum):

    ATTACHMENTS = "attachments"
    AUTHOR_ID = "author_id"
    CONTEXT_ANNOTATIONS = "context_annotations"
    CONVERSATION_ID = "conversation_id"
    CREATED_AT = "created_at"
    ENTITIES = "entities"
    GEO = "geo"
    IN_REPLY_TO_USER_ID = "in_reply_to_user_id"
    LANG = "lang"
    NON_PUBLIC_METRICS = "non_public_metrics"
    PUBLIC_METRICS = "public_metrics"
    ORIGINAL_METRICS = "organic_metrics"
    PROMOTED_METRICS = "promoted_metrics"
    POSSIBLY_SENSITIVE = "possibly_sensitive"
    REFERENCED_TWEET = "referenced_tweets"
    SOURCE = "source"
    WITHHELD = "withheld"

    def __str__(self) -> str:
        return self.value


class Expantion(Enum):

    AUTHOR_ID: str = "author_id"
    REFERENCED_TWEETS_ID: str = "referenced_tweets.id"
    IN_REPLY_TO_USER_ID: str = "in_reply_to_user_id"
    MEDIA_KEYS: str = "attachments.media_keys"
    POLL_IDS: str = "attachments.poll_ids"
    PLACE_ID: str = "geo.place_id"
    MENTIONS_USERNAME: str = "entities.mentions.username"
    REFERENCED_TWEETS_AUTHOR_ID: str = "referenced_tweets.id.author_id"

    def __str__(self) -> str:
        return self.value


class Tweet:
    def __init__(self, id: str, text: str, *args, **kwargs) -> None:
        # Default fields
        self.tweet_id: str = id
        self.text: str = text

        self.additional_fields: Dict = kwargs

        # Additional field
        self.attachments = get_additional_field(kwargs, "attachments")
        self.author_id: Optional[str] = get_additional_field(kwargs, "author_id")
        self.context_annotations = get_additional_field(kwargs, "context_annotations")
        self.conversation_id = get_additional_field(kwargs, "conversation_id")

        self.created_at: Optional[datetime] = None
        if (created_at := get_additional_field(kwargs, "created_at")) is not None:
            self.created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

        self.entities = get_additional_field(kwargs, "entities")
        self.geo = get_additional_field(kwargs, "geo")
        self.in_reply_to_user_id = get_additional_field(kwargs, "in_reply_to_user_id")
        self.lang: Optional[str] = get_additional_field(kwargs, "lang")
        self.non_public_metrics = get_additional_field(kwargs, "non_public_metrics")

        self.public_metrics: Optional[PublicMetric] = None
        public_metrics: Optional[Dict] = get_additional_field(kwargs, "public_metrics")
        if public_metrics:
            self.public_metrics = PublicMetric(public_metrics)

        # self.original_metrics = get_additional_field('organic_metrics')
        # self.promoted_metrics = get_additional_field('promoted_metrics')
        self.possibly_sensitive: Optional[bool] = (
            True
            if get_additional_field(kwargs, "possibly_sensitive") == "true"
            else False
        )
        self.referenced_tweets = get_additional_field(kwargs, "referenced_tweets")
        self.source: Optional[str] = get_additional_field(kwargs, "source")
        self.truncated: Optional[bool] = get_additional_field(kwargs, "truncated")
        self.withheld = get_additional_field(kwargs, "withheld")

        # attachment
        self.medias: Optional[List[Media]] = None
        if "media" in kwargs.keys():
            self.medias = []
            for media in kwargs["media"]:
                self.medias.append(Media(media))

        self.polls: Optional[List[Poll]] = None
        if "polls" in kwargs.keys():
            self.polls = []
            for poll in kwargs["polls"]:
                self.polls.append(Poll(poll))
