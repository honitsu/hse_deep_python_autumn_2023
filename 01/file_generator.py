from io import TextIOWrapper
from typing import List, Iterable, Union


def filter_lines(
    file_input: Union[str, TextIOWrapper],
    words_list: List[str],
    encoding_type: str = "utf-8",
) -> Iterable[str]:
    words = [word.lower() for word in words_list]
    if isinstance(file_input, str):
        # Используем контекстный менеджер для открытия файла
        with open(file_input, "r", encoding=encoding_type) as file:
            for line in file:
                line_words = set(line.lower().split())
                if line_words.intersection(words):
                    yield line.strip()
    else:
        for line in file_input:
            line_words = set(line.lower().split())
            if line_words.intersection(words):
                yield line.strip()
