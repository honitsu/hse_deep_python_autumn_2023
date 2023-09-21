import unittest
from unittest.mock import patch
from unittest import mock
from unittest.mock import MagicMock
import some_model as SomeModel


class TestPredictions(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel.SomeModel()

    @patch("some_model.SomeModel.predict")
    def test_predict_calls(self, predict_mock: MagicMock):
        predict_mock.side_effect = 0.5, 0.5, 0.5

        self.assertEqual(
            SomeModel.predict_message_mood(
                "Очень плохое настроение",
                self.model,
                bad_thresholds=0.9,
                good_thresholds=0.95,
            ),
            "неуд",
        )
        self.assertEqual(
            SomeModel.predict_message_mood(
                "Хорошее настроение", self.model, bad_thresholds=0.4
            ),
            "норм",
        )
        self.assertEqual(
            SomeModel.predict_message_mood(
                "Очень хорошее настроение",
                self.model,
                bad_thresholds=0.2,
                good_thresholds=0.3,
            ),
            "отл",
        )

        expected_calls = [
            mock.call("Очень плохое настроение"),
            mock.call("Хорошее настроение"),
            mock.call("Очень хорошее настроение"),
        ]
        self.assertEqual(expected_calls, predict_mock.mock_calls)

        predict_mock.side_effect = TypeError("Сообщение должно быть строкой")

        with self.assertRaises(TypeError) as ex:
            SomeModel.predict_message_mood(1, self.model)

        self.assertEqual(str(ex.exception), "Сообщение должно быть строкой")

    @patch("some_model.SomeModel.predict")
    def test_bad_threshold(self, predict_mock):
        predict_mock.return_value = 0.1

        self.assertEqual(
            SomeModel.predict_message_mood(
                "Чувствую себя великолепно", self.model
            ),
            "неуд",
        )

    @patch("some_model.SomeModel.predict")
    def test_good_threshold(self, predict_mock):
        predict_mock.return_value = 0.9

        result = SomeModel.predict_message_mood(
            "Чувствую себя великолепно", self.model
        )
        self.assertEqual(result, "отл")

    @patch("some_model.SomeModel.predict")
    def test_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.45

        result = SomeModel.predict_message_mood("Чапаев и Пустота", self.model)
        self.assertEqual(result, "норм")

    def test_equal_thresholds(self):
        with self.assertRaises(ValueError) as context:
            SomeModel.predict_message_mood(
                "Средне",
                self.model,
                bad_thresholds=0.5,
                good_thresholds=0.5,
            )
            self.assertTrue(
                "Верхняя граница должна быть больше нижней"
                in context.exception
            )

    @patch("some_model.SomeModel.predict")
    def test_corner_cases(self, predict_mock):
        predict_mock.side_effect = 0, 0.4, 0.5, 1

        self.assertEqual(
            SomeModel.predict_message_mood("", self.model), "неуд"
        )

        self.assertEqual(
            SomeModel.predict_message_mood("", self.model, bad_thresholds=0.4),
            "норм",
        )
        self.assertEqual(
            SomeModel.predict_message_mood(
                "", self.model, good_thresholds=0.5
            ),
            "норм",
        )
        self.assertEqual(SomeModel.predict_message_mood("", self.model), "отл")

    def test_too_good_thresholds(self):
        self.assertRaises(ValueError)
        with self.assertRaises(ValueError) as context:
            SomeModel.predict_message_mood(
                "Отлинчо", self.model, good_thresholds=1.3
            )
            self.assertTrue(
                "Обе границы должны лежать в диапазоне от 0 до 1"
                in context.exception
            )

    def test_too_bad_thresholds(self):
        with self.assertRaises(ValueError) as context:
            SomeModel.predict_message_mood(
                "Ужасно", self.model, bad_thresholds=-1.3
            )
            self.assertTrue(
                "Обе границы должны лежать в диапазоне от 0 до 1"
                in context.exception
            )

    def test_wrong_thresholds(self):
        with self.assertRaises(ValueError) as context:
            SomeModel.predict_message_mood(
                "Фифти-фифти",
                self.model,
                bad_thresholds=0.6,
                good_thresholds=0.4,
            )
            self.assertTrue(
                "Верхняя граница должна быть больше нижней"
                in context.exception
            )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
