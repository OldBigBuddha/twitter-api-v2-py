from datetime import datetime
from typing import Optional


class Tweet:
    def __init__(self, id: str, text: Optional[str], *args, **kwargs) -> None:
        self.tweet_id: str = id
        self.text: Optional[str] = text
        self.lang: Optional[str] = kwargs['lang']
        self.created_at: Optional[datetime] = datetime.fromisoformat(kwargs['created_at'].replace('Z', '+00:00'))
        self.source: Optional[str] = kwargs['source']
        self.possibly_sensitive: Optional[bool] = True if kwargs['possibly_sensitive'] == 'true' else False
        self.author_id: Optional[str] = kwargs['author_id']
