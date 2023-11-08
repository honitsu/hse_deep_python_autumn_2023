import unittest
import urllib
from queue import Queue
from unittest.mock import MagicMock, patch
from io import BytesIO

from server import (
    read_url,
    HtmlParser,
    master_server
)


class TestWebParser(unittest.TestCase):
    def test_read_url(self):
        url = "http://example.com"
        expected_data = b"{'in': 3, 'Example': 2, 'Domain': 2, 'domain': 2, 'for': 2, 'use': 2, 'This': 1}"

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = BytesIO(expected_data)
            data = read_url(url)
            parser = HtmlParser(7)
            self.assertEqual(parser.get_total(), 0)
            parser.feed(data)
            result = str(parser.most_common_words())

        self.assertEqual(result, expected_data.decode())
        self.assertEqual(parser.get_total(), 1)

    def test_read_url_error(self):
        url = "http://nonexistentexample.com"
        with patch("urllib.request.urlopen"):
            with self.assertRaises(urllib.error.URLError):
                read_url(url)

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

        # self.assertIsNone(parser.error("message"))

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

    def test_html_parser_most_common_words(self):
        words = ["a", "b", "c", "a", "b", "a"]
        k_top = 2
        expected_result = {"a": 3, "b": 2}
        parser = HtmlParser(k_top)
        parser.words = words

        result = parser.most_common_words()

        self.assertEqual(result, expected_result)

    def test_master_server(self):  # pylint: disable=no-self-use
        tasks_queue = Queue()
        sock = unittest.mock.Mock()
        sock.accept.side_effect = [(MagicMock(), None)]
        with unittest.mock.patch("socket.socket", return_value=sock):
            with unittest.mock.patch("os.getpid", return_value=123):
                with unittest.mock.patch("psutil.Process"):
                    master_server(tasks_queue)


if __name__ == "__main__":
    unittest.main()
