from TwitterAPIv2.util import get_additional_field
from enum import Enum
from typing import Optional


class Type(Enum):

    GIF: str = 'GIF'
    PHOTO: str = 'photo'
    VIDEO: str = 'video'

    def __str__(self) -> str:
        return self.value


class Field(Enum):

    HEIGHT: str = 'height'
    WIDTH: str = 'width'
    VIEW_COUNT: str = 'public_metrics'
    DURATION_MS: str = 'duration_ms'
    PREVIEW_IMAGE_URL: str = 'preview_image_url'

    def __str__(self) -> str:
        return self.value


class Media:

    def __init__(self, data: dict) -> None:

        # default
        self.media_key: str = data['media_key']
        self.type: Type = Type(data['type'])

        # additional
        self.height: Optional[int] = get_additional_field(data, Field.HEIGHT.value, int)
        self.width: Optional[int] = get_additional_field(data, Field.WIDTH.value, int)
        self.duration_ms: Optional[int] = get_additional_field(data, Field.DURATION_MS.value, int)
        self.preview_image_url: Optional[str] = get_additional_field(data, Field.PREVIEW_IMAGE_URL.value)

        self.view_count: Optional[int] = None
        public_metric = get_additional_field(data, Field.VIEW_COUNT.value)
        if public_metric:
            self.view_count = int(public_metric['view_count'])
