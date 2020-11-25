from typing import Any, Optional


def get_additional_field(data: dict, key: str, converter=None) -> Optional[Any]:
    if key in data.keys():
        if converter:
            return converter(data[key])
        else:
            # TODO: Use **data[key]
            return data[key]
    else:
        return None
