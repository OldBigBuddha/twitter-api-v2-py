from typing import Any, Optional


def get_additional_field(data: dict, key: str) -> Optional[Any]:
    if key in data.keys():
        return data[key]
    else:
        return None
