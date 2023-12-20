import unittest
from unittest.mock import patch
import asyncio
import pytest
import httpx
import fetcher


# Счётчик строк в файле
@staticmethod
def count_newlines(fname):
    def _make_gen(reader):
        while True:
            buf = reader(2 ** 16)
            if not buf:
                break
            yield buf

    with open(fname, "rb") as file:
        return sum(buf.count(b"\n") for buf in _make_gen(file.raw.read))


# class TestFetchers(unittest.IsolatedAsyncioTestCase):
class TestFetchers(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    @patch("fetcher.httpx.AsyncClient.get", return_value=httpx.Response(200, json={"id": "140315670381952"}))
    def test_fetchers2_10(self, mocker):
        url_file = "10urls.txt"
        lines_in_file = count_newlines(url_file)
        stats = fetcher.start_fetchers(url_file, 2)
        self.assertEqual(stats.get_good(), stats.get_total())
        self.assertEqual(lines_in_file, stats.get_total())
        self.assertEqual(lines_in_file, mocker.call_count)

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    @patch("fetcher.httpx.AsyncClient.get", return_value=httpx.Response(200, json={"id": "140315670381952"}))
    def test_fetchers10_10(self, mocker):
        url_file = "10urls.txt"
        lines_in_file = count_newlines(url_file)
        stats = fetcher.start_fetchers(url_file, 10)
        self.assertEqual(stats.get_good(), stats.get_total())
        self.assertEqual(lines_in_file, stats.get_total())
        self.assertEqual(lines_in_file, mocker.call_count)

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    @patch("fetcher.httpx.AsyncClient.get", return_value=httpx.Response(200, json={"id": "140315670381952"}))
    def test_fetchers3_103(self, mocker):
        url_file = "urls.txt"
        lines_in_file = count_newlines(url_file)
        stats = fetcher.start_fetchers(url_file, 3)
        self.assertEqual(stats.get_good(), stats.get_total())
        self.assertEqual(lines_in_file, stats.get_total())
        self.assertEqual(lines_in_file, mocker.call_count)

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    @patch("fetcher.httpx.AsyncClient.get", return_value=httpx.Response(200, json={"id": "140315670381952"}))
    def test_fetchers10_103(self, mocker):
        url_file = "urls.txt"
        lines_in_file = count_newlines(url_file)
        stats = fetcher.start_fetchers(url_file, 10)
        self.assertEqual(stats.get_good(), stats.get_total())
        self.assertEqual(lines_in_file, stats.get_total())
        self.assertEqual(lines_in_file, mocker.call_count)

    @pytest.mark.asyncio
    @pytest.mark.timeout(5)
    @patch("fetcher.httpx.AsyncClient.get", return_value=httpx.Response(200, json={"id": "140315670381952"}))
    def test_fetchers1000_1kk(self, mocker):
        url_file = "100k_urls.txt"
        lines_in_file = count_newlines(url_file)
        stats = fetcher.start_fetchers(url_file, 1000)
        self.assertEqual(stats.get_good(), stats.get_total())
        self.assertEqual(lines_in_file, stats.get_total())
        self.assertEqual(lines_in_file, mocker.call_count)


if __name__ == "__main__":
    unittest.main()
