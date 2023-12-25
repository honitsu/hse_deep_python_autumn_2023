#!/usr/bin/env python3
# test_fetcher.py

import unittest
from unittest.mock import patch
import asyncio
import httpx
import fetcher


# Быстрый счётчик строк в файле
def count_newlines(fname):
    def _make_gen(reader):
        while True:
            buf = reader(2 ** 16)
            if not buf:
                break
            yield buf

    with open(fname, "rb") as file:
        return sum(buf.count(b"\n") for buf in _make_gen(file.raw.read))


async def fake_reply(url):
    await asyncio.sleep(0)
    if url[4] == ":":
        return httpx.Response(301, json={"id": "140315670381950"})
    if url[9] == "w":
        return httpx.Response(403, json={"id": "140315670381951"})
    return httpx.Response(200, json={"id": "140315670381952"})


class TestFetchers(unittest.IsolatedAsyncioTestCase):
    async def test_single_get(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            URL1 = 'https://www.adobe.com/ru/'
            URL2 = 'https://ar.wikipedia.org'
            async with httpx.AsyncClient() as session:
                ret = await fetcher.fetch_url(session, URL1)
                self.assertEqual(ret, ('https://www.adobe.com/ru/', 403, 'Forbidden'))
                ret = await fetcher.fetch_url(session, URL2)
                self.assertEqual(ret, ('https://ar.wikipedia.org', 200, 'OK'))

    async def test_01workers_010urls(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            url_file = "10urls.txt"
            ret = await fetcher.start_fetchers(url_file, 1)
            expected_ret = []
            self.assertEqual(count_newlines(url_file), mocker.call_count)
            # Проверяем содержание отправленных запросов
            with open(url_file, "r", encoding="utf-8") as file:
                for url in file:
                    url = url.rstrip()
                    mocker.assert_any_call(url)
                    fret = await fake_reply(url)
                    expected_ret.append((url, fret.status_code, fret.reason_phrase))
            self.assertEqual(expected_ret, ret)

    async def test_02workers_010urls(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            url_file = "10urls.txt"
            ret = await fetcher.start_fetchers(url_file, 2)
            expected_ret = []
            self.assertEqual(count_newlines(url_file), mocker.call_count)
            # Проверяем содержание отправленных запросов
            with open(url_file, "r", encoding="utf-8") as file:
                for url in file:
                    url = url.rstrip()
                    mocker.assert_any_call(url)
                    fret = await fake_reply(url)
                    expected_ret.append((url, fret.status_code, fret.reason_phrase))
            self.assertEqual(sorted(expected_ret), sorted(ret))

    async def test_10workers_010urls(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            url_file = "10urls.txt"
            ret = await fetcher.start_fetchers(url_file, 10)
            expected_ret = []
            self.assertEqual(count_newlines(url_file), mocker.call_count)
            # Проверяем содержание отправленных запросов
            with open(url_file, "r", encoding="utf-8") as file:
                for url in file:
                    url = url.rstrip()
                    mocker.assert_any_call(url)
                    fret = await fake_reply(url)
                    expected_ret.append((url, fret.status_code, fret.reason_phrase))
            self.assertEqual(sorted(expected_ret), sorted(ret))

    async def test_03workers_100urls(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            url_file = "urls.txt"
            ret = await fetcher.start_fetchers(url_file, 3)
            expected_ret = []
            self.assertEqual(count_newlines(url_file), mocker.call_count)
            # Проверяем содержание отправленных запросов
            with open(url_file, "r", encoding="utf-8") as file:
                for url in file:
                    url = url.rstrip()
                    mocker.assert_any_call(url)
                    fret = await fake_reply(url)
                    expected_ret.append((url, fret.status_code, fret.reason_phrase))
            self.assertEqual(sorted(expected_ret), sorted(ret))

    async def test_13workers_100urls(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            url_file = "urls.txt"
            ret = await fetcher.start_fetchers(url_file, 13)
            expected_ret = []
            self.assertEqual(count_newlines(url_file), mocker.call_count)
            # Проверяем содержание отправленных запросов
            with open(url_file, "r", encoding="utf-8") as file:
                for url in file:
                    url = url.rstrip()
                    mocker.assert_any_call(url)
                    fret = await fake_reply(url)
                    expected_ret.append((url, fret.status_code, fret.reason_phrase))
            self.assertEqual(sorted(expected_ret), sorted(ret))

    '''
    async def test_25workers_1k_urls(self):
        with patch("fetcher.httpx.AsyncClient.get", side_effect=fake_reply) as mocker:
            url_file = "1k_urls.txt"
            ret = await fetcher.start_fetchers(url_file, 25)
            expected_ret = []
            self.assertEqual(count_newlines(url_file), mocker.call_count)
            # Проверяем содержание отправленных запросов
            with open(url_file, "r", encoding="utf-8") as file:
                for url in file:
                    url = url.rstrip()
                    mocker.assert_any_call(url)
                    fret = await fake_reply(url)
                    expected_ret.append((url, fret.status_code, fret.reason_phrase))
            self.assertEqual(sorted(expected_ret), sorted(ret))
    '''


if __name__ == "__main__":
    unittest.main()
