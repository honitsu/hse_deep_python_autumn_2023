#!/usr/bin/env python3
# test_server.py

import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
import threading
from server import read_url, HtmlParser
import server


class TestWebParser(unittest.TestCase):
    def test_read_url(self):
        url = "http://sample.com"
        expected_data = b"{'in': 3, 'Example': 2}"

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = BytesIO(expected_data)
            data = read_url(url)
            parser = HtmlParser(2)
            self.assertEqual(parser.get_total(), 0)
            parser.feed(str(data))
            str(parser.most_common_words())

        self.assertEqual(data, expected_data)
        self.assertEqual(parser.get_total(), 1)

    def test_html_parser_init(self):
        k_top = 10
        parser = HtmlParser(k_top)

        self.assertEqual(parser.curr_tag, "")
        self.assertEqual(parser.k_top, k_top)
        self.assertEqual(parser.get_total(), 0)
        self.assertEqual(len(parser.words), 0)

    def test_html_parser_error(self):
        with self.assertRaises(TypeError):
            HtmlParser()  # pylint: disable=no-value-for-parameter

    def test_html_parser_feed(self):
        data = "<html><body><h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p></body></html>"
        expected_words = ["Title", "Paragraph", "1", "Paragraph", "2"]
        parser = HtmlParser(7)

        parser.feed(data)

        self.assertEqual(parser.words, expected_words)
        self.assertEqual(parser.get_total(), 1)

    def test_html_parser_handle_starttag(self):
        tag = "h1"
        parser = HtmlParser(7)

        parser.handle_starttag(tag, None)

        self.assertEqual(parser.curr_tag, tag)

    def test_html_parser_handle_data(self):
        data = "Some text"
        parser = HtmlParser(7)
        parser.curr_tag = "p"

        parser.handle_data(data)

        self.assertEqual(parser.words, data.split())

    def test_workers(self):
        num_wrk = 10
        mock_thread = MagicMock(spec=threading.Thread)
        with patch("threading.Thread") as mock_thread:
            custom_parser = HtmlParser(7)
            server.start_workers(num_wrk, custom_parser)
        self.assertEqual(mock_thread.call_count, num_wrk + 1)

    def test_html_parser_most_common_words(self):
        words = ["a", "b", "c", "a", "b", "a"]
        k_top = 2
        expected_result = {"a": 3, "b": 2}
        parser = HtmlParser(k_top)
        parser.words = words

        result = parser.most_common_words()

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
