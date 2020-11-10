from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from TwitterAPIv2.util import get_additional_field


class Status(Enum):

    OPEN: str = 'open'
    CLOSED: str = 'closed'

    def __str__(self) -> str:
        return self.value


class Option:

    def __init__(self, data: Dict) -> None:
        self.position: int = int(data['position'])
        self.label: str = data['label']
        self.votes: int = data['votes']


class Field(Enum):

    DURATION_MINUTES: str = 'duration_minutes'
    END_DATETIME: str = 'end_datetime'
    VOTING_STATUS: str = 'voting_status'

    def __str__(self) -> str:
        return self.value


class Poll:

    def __init__(self, data: Dict) -> None:
        # default
        self.id: str = data['id']
        self.options: List[Option] = []
        for option in data['options']:
            self.options.append(Option(option))

        # additional
        self.duration_minutes: Optional[int] = get_additional_field(data, 'duration_minutes', int)
        self.end_datetime: Optional[datetime] = None
        if (end_datetime := get_additional_field(data, 'end_datetime')) is not None:
            self.end_datetime = datetime.fromisoformat(end_datetime.replace('Z', '+00:00'))
        self.voting_status: Optional[Status] = get_additional_field(data, 'voting_status', Status)
