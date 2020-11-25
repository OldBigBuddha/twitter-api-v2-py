import logging
from datetime import datetime
from enum import Enum
from logging import Logger
from typing import Dict, List, Optional, Tuple

from twitter_api_v2 import ContextAnnotation, Entity
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


class Entities:
    def __init__(self) -> None:
        self.annotations: Optional[List[Entity.Annotation]] = None
        self.cashtags: Optional[List[Entity.CashTag]] = None
        self.hashtags: Optional[List[Entity.HashTag]] = None
        self.mentions: Optional[List[Entity.Mention]] = None
        self.urls: Optional[List[Entity.Url]] = None


class Tweet:
    def __init__(self, id: str, text: str, *args, **kwargs) -> None:

        self.logger: Logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Default fields
        self.id: str = id
        self.text: str = text

        # Additional field
        self.author_id: Optional[str] = get_additional_field(kwargs, "author_id")

        # self.context_annotations = get_additional_field(kwargs, "context_annotations")
        self.context_annotations: Optional[
            List[
                Tuple[
                    Optional[ContextAnnotation.Domain],
                    Optional[ContextAnnotation.Entity],
                ]
            ]
        ] = None
        if "context_annotations" in kwargs.keys():
            self.context_annotations = []
            for context_annotation_res in kwargs["context_annotations"]:
                domain: Optional[ContextAnnotation.Domain] = None
                if (
                    domain_res := get_additional_field(context_annotation_res, "domain")
                ) :
                    domain = ContextAnnotation.Domain(
                        domain_res["id"],
                        domain_res["name"],
                        get_additional_field(domain_res, "description"),
                    )

                context_entity: Optional[ContextAnnotation.Entity] = None
                if (
                    entity_res := get_additional_field(context_annotation_res, "entity")
                ) :
                    context_entity = ContextAnnotation.Entity(
                        entity_res["id"],
                        entity_res["name"],
                        get_additional_field(entity_res, "description"),
                    )

                self.context_annotations.append((domain, context_entity))

        self.conversation_id = get_additional_field(kwargs, "conversation_id")

        self.created_at: Optional[datetime] = None
        if (created_at := get_additional_field(kwargs, "created_at")) is not None:
            self.created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

        # TODO: Implement entities
        self.entities: Optional[Entities] = None
        if "entities" in kwargs.keys():
            tweet_entities: Entities = Entities()
            entities_res: Dict = kwargs["entities"]

            if "annotations" in entities_res.keys():
                tweet_entities.annotations = []
                annotations: List[Dict] = entities_res["annotations"]
                for annotation in annotations:
                    tweet_entities.annotations.append(
                        Entity.Annotation(
                            annotation["start"],
                            annotation["end"],
                            annotation["probability"],
                            annotation["type"],
                            annotation["normalized_text"],
                        )
                    )

            if "cashtags" in entities_res.keys():
                tweet_entities.cashtags = []
                cashtags: List[Dict] = entities_res["cashtags"]
                for cashtag in cashtags:
                    tweet_entities.cashtags.append(
                        Entity.CashTag(cashtag["start"], cashtag["end"], cashtag["tag"])
                    )

            if "hashtags" in entities_res.keys():
                tweet_entities.hashtags = []
                hashtags: List[Dict] = entities_res["hashtags"]
                for hashtag in hashtags:
                    tweet_entities.hashtags.append(
                        Entity.HashTag(hashtag["start"], hashtag["end"], hashtag["tag"])
                    )

            if "mentions" in entities_res.keys():
                tweet_entities.mentions = []
                mentions: List[Dict] = entities_res["mentions"]
                for mention in mentions:
                    tweet_entities.mentions.append(
                        Entity.Mention(mention["start"], mention["end"], mention["tag"])
                    )

            if "urls" in entities_res.keys():
                tweet_entities.urls = []
                urls: List[Dict] = entities_res["urls"]
                for url in urls:
                    tweet_entities.urls.append(
                        Entity.Url(
                            url["start"],
                            url["end"],
                            url["url"],
                            url["expanded_url"],
                            url["display_url"],
                        )
                    )

            self.entities = tweet_entities

        # TODO: Implement Place Object
        self.geo = get_additional_field(kwargs, "geo")

        self.in_reply_to_user_id: Optional[str] = get_additional_field(
            kwargs, "in_reply_to_user_id"
        )
        self.lang: Optional[str] = get_additional_field(kwargs, "lang")

        self.public_metrics: Optional[PublicMetric] = get_additional_field(
            kwargs, "public_metrics", PublicMetric
        )

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
