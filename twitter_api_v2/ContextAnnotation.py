from typing import Optional


class Domain:
    def __init__(self, id: str, name: str, description: Optional[str] = None) -> None:
        self.id: str = id
        self.name: str = name
        self.description: Optional[str] = description


class Entity:
    def __init__(self, id: str, name: str, description: Optional[str] = None) -> None:
        self.id: str = id
        self.name: str = name
        self.description: Optional[str] = description
