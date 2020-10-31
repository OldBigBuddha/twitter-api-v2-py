from enum import Enum
from datetime import datetime
from typing import Optional


class Field(Enum):

    ATTACHMENTS = 'attachments',
    AUTHOR_ID = 'author_id',
    CONTEXT_ANNOTATIONS = 'context_annotations',
    CONVERSATION_ID = 'conversation_id',
    CREATED_AT = 'created_at',
    ENTITIES = 'entities',
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


class Tweet:

    def __init__(self, id: str, text: str, created_at: str, source: str, *args, **kwargs) -> None:
        self.tweet_id: str = id
        self.text: str = text
        self.created_at: datetime = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        self.source: str = source
        self.lang: Optional[str] = kwargs['lang']
        self.possibly_sensitive: Optional[bool] = True if kwargs['possibly_sensitive'] == 'true' else False
        self.author_id: Optional[str] = kwargs['author_id']
