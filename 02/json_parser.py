import json
from typing import Optional, List


def callback(key: str, word: str) -> None:
    print(f"{key}: {word}")


def parse_json(
    json_str: str,
    required_fields: Optional[List[str]] = None,
    keywords: Optional[List[str]] = None,
    keyword_callback=callback,
) -> None:
    if keyword_callback is None:
        raise TypeError("Функция-обработчик не может быть None")

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Передана невалидная JSON-строка") from exc

    if not required_fields:
        required_fields = list(data.keys())

    for field in required_fields:
        if field not in data:
            continue

        if keywords:
            for word in filter(lambda w: w in keywords, data[field].split()):
                keyword_callback(field, word)
        else:
            for word in data[field].split():
                keyword_callback(field, word)
