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
        file = open(  # pylint: disable=consider-using-with
            file_input, "r", encoding=encoding_type
        )
    else:
        file = file_input
    for line in file:
        line_words = set(line.lower().split())
        if line_words.intersection(words):
            yield line.strip()
    if isinstance(file_input, str):
        file.close()
