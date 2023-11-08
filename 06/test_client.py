import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
import socket
from client import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(target_address="localhost")
        self.client.urls_queue = Queue()

    def test_send_request(self):
        mock_socket = MagicMock(spec=socket.socket)
        mock_socket.recv.return_value = b"Test response"
        mock_socket.connect.return_value = None

        with patch("socket.socket", return_value=mock_socket):
            self.client.urls_queue.put("http://example.com")
            self.client.urls_queue.put("EOF")
            self.client.send_request()

        self.assertEqual(mock_socket.sendall.call_count, 2)
        self.assertEqual(mock_socket.recv.call_count, 1)
        self.assertEqual(mock_socket.recv.call_args[0][0], 1024)

    def test_read_urls_from_file(self):
        test_urls = ["http://example1.com", "http://example2.com"]
        with open("test_urls.txt", "w", encoding="utf-8") as file:
            for url in test_urls:
                file.write(url + "\n")

        self.client.read_urls_from_file("test_urls.txt")

        self.assertEqual(self.client.urls_queue.qsize(), len(test_urls) + 1)

    def test_read_nonexistent_url(self):
        nonexistent_url = "http://nonexistenturl.com"
        with open("test_urls.txt", "w", encoding="utf-8") as file:
            file.write(nonexistent_url)

        self.client.read_urls_from_file("test_urls.txt")

        self.assertEqual(self.client.urls_queue.qsize(), 2)
        self.assertEqual(self.client.urls_queue.get(), nonexistent_url)

    def test_start_threads(self):
        self.client.send_request = MagicMock()

        self.client.start_threads(3)

        self.assertEqual(self.client.send_request.call_count, 3)


if __name__ == "__main__":
    unittest.main()
