from abc import ABCMeta
from enum import Enum
from typing import Optional, Tuple


class Entity(metaclass=ABCMeta):
    pass


class Annotation(Entity):
    def __init__(
        self, start: int, end: int, probability: float, type: str, normalized_text: str
    ) -> None:

        self.start: int = start
        self.end: int = end

        self.normalized_text: str = normalized_text
        self.probability: float = probability
        self.type: str = type


class CashTag:
    def __init__(self, start: int, end: int, tag: str) -> None:

        self.start: int = start
        self.end: int = end

        self.tag: str = tag


class HashTag:
    def __init__(self, start: int, end: int, tag: str) -> None:

        self.start: int = start
        self.end: int = end

        self.tag: str = tag


class Mention:
    def __init__(self, start: int, end: int, tag: str) -> None:

        self.start: int = start
        self.end: int = end

        self.tag: str = tag


class Url:
    def __init__(
        self, start: int, end: int, url: str, expanded_url: str, display_url: str
    ) -> None:

        self.start: int = start
        self.end: int = end

        self.url: str = url
        self.expanded_url: str = expanded_url
        self.display_url: str = display_url


class Size:
    def __init__(self, w: int, h: int, resize: str) -> None:

        self.h: int = h
        self.w: int = w
        self.resize: str = resize


class Sizes:
    def __init__(self, thumb: Size, small: Size, medium: Size, large: Size) -> None:

        self.thumb: Size = thumb
        self.small: Size = small
        self.medium: Size = medium
        self.large: Size = large


class MediaType(Enum):
    ANIMATED_GIF = ("animated_gif",)
    PHOTO = ("photo",)
    VIDEO = "video"


class Media(Entity):
    def __init__(self, obj: dict) -> None:

        self.display_url: str = obj["display_url"]
        self.expanded_url: str = obj["expanded_url"]
        self.media_id: str = obj["id_str"]
        self.indices: Tuple[int, int] = obj["indices"]
        self.media_url: str = obj["media_url_https"]

        sizes: Sizes = Sizes(
            Size(**obj["sizes"]["thumb"]),
            Size(**obj["sizes"]["small"]),
            Size(**obj["sizes"]["medium"]),
            Size(**obj["sizes"]["large"]),
        )
        self.sizes = sizes

        self.source_status_id: Optional[str] = (
            obj["source_status_id_str"] if "source_status_id" in obj.keys() else None
        )
        self.type: MediaType = MediaType(obj["type"])
        self.url: str = obj["url"]
