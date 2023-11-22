import unittest
from unittest.mock import Mock
import asyncio
import aiohttp
import fetcher


class TestInfo(unittest.TestCase):
    stats = fetcher.Info()

    def test_add_good(self):
        self.stats.add_good()
        self.assertEqual(self.stats.get_good(), 1)

    def test_add_bad(self):
        self.stats.add_bad()
        self.stats.add_bad()
        self.assertEqual(self.stats.get_bad(), 2)

    def test_add_total(self):
        self.assertEqual(self.stats.get_total(), 3)

    def setUp(self):
        self.urls = [
            "https://example.com",
            "https://mail.ru",
            "https://2ip.ru",
            "https://amazon.de",
        ]
        self.concurrent_requests = 2
        self.session_mock = Mock(spec=aiohttp.ClientSession)
        self.loop = asyncio.get_event_loop()

    def test_fetch_urls(self):
        mock_results = [
            "This domain is for use in illustrative examples in documents.",
            "* @param {*} s Имя метрики, если прилетает не стринга, то это как бы коммит,"
            " все собранные радары дёргаются в одном запросе",
            "Анонимайзер",
            "Wir helfen dir</div>",
        ]

        results = self.loop.run_until_complete(
            fetcher.fetch_urls(self.urls, self.concurrent_requests, self.stats)
        )
        self.assertEqual(results[0].count(mock_results[0]), 1)
        self.assertEqual(results[1].count(mock_results[1]), 1)
        self.assertEqual(results[2].count(mock_results[2]), 1)
        self.assertEqual(results[3].count(mock_results[3]), 1)
        self.assertEqual(self.stats.get_good(), 5)

    def test_fetch_invalid_urls(self):
        self.urls = [
            "https://docs.aiohttp.org/en/stable/client_ref.html",
            "https://sarkariresult.com",
        ]
        results = self.loop.run_until_complete(
            fetcher.fetch_urls(self.urls, self.concurrent_requests, self.stats)
        )
        self.assertEqual(results[0], "Error: 404")
        self.assertEqual(results[1], "Error: 403")
        self.assertEqual(self.stats.get_bad(), 4)

    def test_fetch_no_urls(self):
        self.concurrent_requests = 0
        self.urls = []
        save_good = self.stats.get_good()
        save_bad = self.stats.get_bad()
        save_total = self.stats.get_total()
        self.loop.run_until_complete(
            fetcher.fetch_urls(self.urls, self.concurrent_requests, self.stats)
        )
        self.assertEqual(self.stats.get_good(), save_good)
        self.assertEqual(self.stats.get_bad(), save_bad)
        self.assertEqual(self.stats.get_total(), save_total)

    def test_read_urls_list(self):
        urls_file = "test_urls.txt"
        urls = fetcher.read_urls_list(urls_file)
        self.assertEqual(
            urls,
            [
                "https://2ip.ru",
                "https://amazon.de",
                "https://example.com",
                "https://github.com",
                "https://google.com",
            ],
        )


if __name__ == "__main__":
    unittest.main()
