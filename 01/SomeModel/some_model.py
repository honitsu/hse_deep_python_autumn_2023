"""
    Реализовать функцию predict_message_mood,
    которая приниамает на вход строку,
    экземпляр модели SomeModel и пороги хорошести.
"""


class SomeModel:
    def predict(self, message: str) -> float:
        # реализация не важна
        pass


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """Функция возвращает:
    - "неуд", если предсказание модели меньше bad_threshold
    - "отл", если предсказание модели больше good_threshold
    - "норм" в остальных случаях
    """
    if bad_thresholds >= good_thresholds:
        raise ValueError(
            "Значение bad_threshold " "должно быть меньше good_threshold"
        )
    if bad_thresholds < 0 or good_thresholds > 1:
        raise ValueError("Значение должны быть в пределах от 0 до 1")

    mood = model.predict(message)

    if mood < bad_thresholds:
        return "неуд"
    if mood > good_thresholds:
        return "отл"
    return "норм"
