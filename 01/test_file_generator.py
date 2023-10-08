import unittest
import os
from file_generator import filter_lines

TESTFILENAME = "words_file.txt"


class TestFilterLines(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(TESTFILENAME, "w", encoding="utf-8") as file:
            file.write(
                "Hello there\nThis is a default phrase\n"
                "For testing the file\n"
            )

    # @classmethod
    # def tearDownClass(cls) -> None:
    #    os.remove(TESTFILENAME)

    def test_several_matches(self):
        filterwords = ["Hello", "phrase", "testing"]
        expected_result = [
            "Hello there",
            "This is a default phrase",
            "For testing the file",
        ]
        result = list(filter_lines(TESTFILENAME, filterwords))
        self.assertEqual(result, expected_result)

        with open(TESTFILENAME, "r", encoding="utf-8") as fileobj:
            result = list(filter_lines(fileobj, filterwords))
            self.assertEqual(result, expected_result)

    def test_no_match(self):
        filterwords = ["I'm", "so", "sorry", "no", "matches"]
        result = list(filter_lines(TESTFILENAME, filterwords))
        self.assertEqual(result, [])

        with open(TESTFILENAME, "r", encoding="utf-8") as fileobj:
            result = list(filter_lines(fileobj, filterwords))
            self.assertEqual(result, [])

    def test_empty_file(self):
        filename = "empty_file.txt"
        filterwords = ["Hello", "phrase", "testing"]
        with open(filename, "w", encoding="utf-8"):
            pass

        results = list(filter_lines(filename, filterwords))
        self.assertEqual(results, [])

        with open(filename, "r", encoding="utf-8") as fileobj:
            results = list(filter_lines(fileobj, filterwords))
            self.assertEqual(results, [])

        os.remove(filename)

    def test_close_but_no_matches(self):
        filterwords = ["Hi", "defolt", "frase"]
        result = list(filter_lines(TESTFILENAME, filterwords))
        self.assertEqual(result, [])

        with open(TESTFILENAME, "r", encoding="utf-8") as fileobj:
            result = list(filter_lines(fileobj, filterwords))
            self.assertEqual(result, [])

    def test_no_filterwords(self):
        result = list(filter_lines(TESTFILENAME, []))
        self.assertEqual(result, [])

        with open(TESTFILENAME, "r", encoding="utf-8") as fileobj:
            result = list(filter_lines(fileobj, []))
            self.assertEqual(result, [])

    def test_wrong_case(self):
        filterwords = ["hello", "PHRASE", "TestinG"]
        expected_result = [
            "Hello there",
            "This is a default phrase",
            "For testing the file",
        ]
        result = list(filter_lines(TESTFILENAME, filterwords))
        self.assertEqual(result, expected_result)


def main():
    unittest.main()
    # var1 = filter_lines('test.txt', ('охотник',))
    # print(next(var1))


if __name__ == "__main__":
    main()
