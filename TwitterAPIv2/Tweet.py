from enum import Enum
from datetime import datetime
from typing import Any, Optional

from TwitterAPIv2.util import get_additional_field
from TwitterAPIv2.Metric import PublicMetric


class Field(Enum):

    ATTACHMENTS = 'attachments'
    AUTHOR_ID = 'author_id'
    CONTEXT_ANNOTATIONS = 'context_annotations'
    CONVERSATION_ID = 'conversation_id'
    CREATED_AT = 'created_at'
    ENTITIES = 'entities'
    GEO = 'geo'
    IN_REPLY_TO_USER_ID = 'in_reply_to_user_id'
    LANG = 'lang'
    NON_PUBLIC_METRICS = 'non_public_metrics'
    PUBLIC_METRICS = 'public_metrics'
    ORIGINAL_METRICS = 'organic_metrics'
    PROMOTED_METRICS = 'promoted_metrics'
    POSSIBLY_SENSITIVE = 'possibly_sensitive'
    REFERENCED_TWEET = 'referenced_tweets'
    SOURCE = 'source'
    WITHHELD = 'withheld'

    def __str__(self) -> str:
        return self.value


class Tweet:

    def __init__(self, id: str, text: str, *args, **kwargs) -> None:
        # Default fields
        self.tweet_id: str = id
        self.text: str = text

        self.additional_fields: dict = kwargs

        # Additional field
        self.attachments = get_additional_field(kwargs, 'attachments')
        self.author_id: Optional[str] = get_additional_field(kwargs, 'author_id')
        self.context_annotations = get_additional_field(kwargs, 'context_annotations')
        self.conversation_id = get_additional_field(kwargs, 'conversation_id')

        self.created_at: Optional[datetime] = None
        if (created_at := get_additional_field(kwargs, 'created_at')) is not None:
            self.created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

        self.entities = get_additional_field(kwargs, 'entities')
        self.geo = get_additional_field(kwargs, 'geo')
        self.in_reply_to_user_id = get_additional_field(kwargs, 'in_reply_to_user_id')
        self.lang: Optional[str] = get_additional_field(kwargs, 'lang')
        self.non_public_metrics = get_additional_field(kwargs, 'non_public_metrics')

        self.public_metrics: Optional[PublicMetric] = None
        public_metrics: Optional[dict] = get_additional_field(kwargs, 'public_metrics')
        if public_metrics:
            self.public_metrics = PublicMetric(public_metrics)

        # self.original_metrics = get_additional_field('organic_metrics')
        # self.promoted_metrics = get_additional_field('promoted_metrics')
        self.possibly_sensitive: Optional[bool] = True if get_additional_field(kwargs, 'possibly_sensitive') == 'true' else False
        self.referenced_tweets = get_additional_field(kwargs, 'referenced_tweets')
        self.source: Optional[str] = get_additional_field(kwargs, 'source')
        self.truncated: Optional[bool] = get_additional_field(kwargs, 'truncated')
        self.withheld = get_additional_field(kwargs, 'withheld')
