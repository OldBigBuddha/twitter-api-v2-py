from enum import Enum
from datetime import datetime
from typing import Any, Optional

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
        self.attachments = self.get_additional_field('attachments')
        self.author_id: Optional[str] = self.get_additional_field('author_id')
        self.context_annotations = self.get_additional_field('context_annotations')
        self.conversation_id = self.get_additional_field('conversation_id')

        self.created_at: Optional[datetime] = None
        if (created_at := self.get_additional_field('created_at')) is not None:
            self.created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

        self.entities = self.get_additional_field('entities')
        self.geo = self.get_additional_field('geo')
        self.in_reply_to_user_id = self.get_additional_field('in_reply_to_user_id')
        self.lang: Optional[str] = self.get_additional_field('lang')
        self.non_public_metrics = self.get_additional_field('non_public_metrics')

        self.public_metrics: Optional[PublicMetric] = None
        public_metrics: Optional[dict] = self.get_additional_field('public_metrics')
        if public_metrics:
            self.public_metrics = PublicMetric(public_metrics)

        # self.original_metrics = self.get_additional_field('organic_metrics')
        # self.promoted_metrics = self.get_additional_field('promoted_metrics')
        self.possibly_sensitive: Optional[bool] = True if self.get_additional_field('possibly_sensitive') == 'true' else False
        self.referenced_tweets = self.get_additional_field('referenced_tweets')
        self.source: Optional[str] = self.get_additional_field('source')
        self.truncated: Optional[bool] = self.get_additional_field('truncated')
        self.withheld = self.get_additional_field('withheld')

    def get_additional_field(self, key: str) -> Optional[Any]:
        if key in self.additional_fields.keys():
            return self.additional_fields[key]
        else:
            return None
