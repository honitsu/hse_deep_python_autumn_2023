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
            SomeModel.predict_message_mood("Чувствую себя великолепно", self.model),
            "неуд",
        )

    @patch("some_model.SomeModel.predict")
    def test_good_threshold(self, predict_mock):
        predict_mock.return_value = 0.9

        result = SomeModel.predict_message_mood("Чувствую себя великолепно", self.model)
        self.assertEqual(result, "отл")

    @patch("some_model.SomeModel.predict")
    def test_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.45

        result = SomeModel.predict_message_mood("Чапаев и Пустота", self.model)
        self.assertEqual(result, "норм")

    def test_equal_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Значение bad_threshold должно быть меньше good_threshold"
        ):
            SomeModel.predict_message_mood(
                "Средне",
                self.model,
                bad_thresholds=0.5,
                good_thresholds=0.5,
            )

    @patch("some_model.SomeModel.predict")
    def test_zero_threshold(self, predict_mock):
        predict_mock.return_value = 0
        result = SomeModel.predict_message_mood("Хуже не бывает", self.model)
        self.assertEqual(result, "неуд")

    @patch("some_model.SomeModel.predict")
    def test_near_zero_threshold(self, predict_mock):
        predict_mock.return_value = 0.0001
        result = SomeModel.predict_message_mood("Очень и очень плохо", self.model)
        self.assertEqual(result, "неуд")

    @patch("some_model.SomeModel.predict")
    def test_lower_than_lowest_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.2999
        result = SomeModel.predict_message_mood("Почти удовлетворительно", self.model)
        self.assertEqual(result, "неуд")

    @patch("some_model.SomeModel.predict")
    def test_lowest_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.3
        result = SomeModel.predict_message_mood(
            "Удовлетворительно по нижней границе", self.model
        )
        self.assertEqual(result, "норм")

    @patch("some_model.SomeModel.predict")
    def test_higher_than_lowest_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.3001
        result = SomeModel.predict_message_mood(
            "Чуть выше нижней удовлетворительной границы", self.model
        )
        self.assertEqual(result, "норм")

    @patch("some_model.SomeModel.predict")
    def test_lower_than_highest_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.7999
        result = SomeModel.predict_message_mood("Почти хорошо", self.model)
        self.assertEqual(result, "норм")

    @patch("some_model.SomeModel.predict")
    def test_highest_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.8
        result = SomeModel.predict_message_mood("Уже почти хорошо", self.model)
        self.assertEqual(result, "норм")

    @patch("some_model.SomeModel.predict")
    def test_higher_than_highest_normal_threshold(self, predict_mock):
        predict_mock.return_value = 0.8001
        result = SomeModel.predict_message_mood("Уже хорошо", self.model)
        self.assertEqual(result, "отл")

    @patch("some_model.SomeModel.predict")
    def test_near_one_threshold(self, predict_mock):
        predict_mock.return_value = 0.9999
        result = SomeModel.predict_message_mood("Почти идеально", self.model)
        self.assertEqual(result, "отл")

    @patch("some_model.SomeModel.predict")
    def test_one_threshold(self, predict_mock):
        predict_mock.return_value = 1
        result = SomeModel.predict_message_mood("Идеально", self.model)
        self.assertEqual(result, "отл")

    def test_too_good_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Обе границы должны лежать в диапазоне от 0 до 1"
        ):
            SomeModel.predict_message_mood("Отлинчо", self.model, good_thresholds=1.3)

    def test_too_bad_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Обе границы должны лежать в диапазоне от 0 до 1"
        ):
            SomeModel.predict_message_mood("Ужасно", self.model, bad_thresholds=-1.3)

    def test_wrong_thresholds(self):
        with self.assertRaisesRegex(
            ValueError, "Значение bad_threshold должно быть меньше good_threshold"
        ):
            SomeModel.predict_message_mood(
                "Фифти-фифти",
                self.model,
                bad_thresholds=0.6,
                good_thresholds=0.4,
            )


def main():
    unittest.main()


if __name__ == "__main__":
    main()
