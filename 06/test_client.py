# test_client.py

import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
import socket
from client import Client


class TestClient(unittest.TestCase):
    # Значения по умолчанию при запуске без аргументов
    urls_file = "urls.txt"
    workers = 2

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

    def setUp(self):
        self.client = None
        self.urls_file_lines = self.count_newlines(self.urls_file)

    def test_client_init(self):
        client = Client(target_address="localhost:12334", urls_file="urls.txt", workers=10)
        self.assertEqual(client.workers, 10)
        self.assertEqual(client.urls_file, "urls.txt")
        self.assertEqual(client.target_address, "localhost")
        self.assertEqual(client.tcp_port, 12334)
        self.assertEqual(client.th_count, 0)
        self.assertTrue(client.show_output)

    def test_invalid_file(self):
        client = Client(target_address="localhost", urls_file="no-such-file.txt", workers=2)
        with self.assertRaises(Exception):
            client.read_urls_from_file()

    def test_invalid_workers(self):
        with self.assertRaises(Exception):
            Client(target_address="localhost", urls_file="urls.txt", workers=0)

    def test_start_threads(self):
        # Запускаем многократно, меняя число потоков
        for num_workers in (2, 3, 5, 7):
            if num_workers == 2:
                self.client = Client(target_address="localhost", urls_file=self.urls_file, workers=num_workers)
            else:
                self.client = Client(target_address="localhost:12345", urls_file=self.urls_file, workers=num_workers)
            print(self.client.workers)
            self.client.urls_queue = Queue()
            # При запуске в 2 потока выводим строки на экран
            if self.client.workers > 2:
                self.client.show_output = False

            self.client.url_process = MagicMock()
            mock_socket = MagicMock(spec=socket.socket)
            with patch("socket.socket", return_value=mock_socket):
                mock_socket.recv.return_value = b"{'Pseudo': 3, 'Values': 2}"
                mock_socket.connect.return_value = None
                mock_socket.close.return_value = None
                self.client.start_threads()

            # Счётчик подключений
            self.assertEqual(mock_socket.connect.call_count, self.urls_file_lines + 1)
            # Счётчик отправленных запросов
            self.assertEqual(mock_socket.sendall.call_count, self.urls_file_lines + 1)
            # Счётчик принятых ответов
            self.assertEqual(mock_socket.recv.call_count, self.urls_file_lines)
            # Число потоков + 1 (дополнительный поток читает url из файла и отправляет на обработку)
            self.assertEqual(self.client.th_count, self.client.workers + 1)
            # Счётчик прочитанных строк из файла с URL
            self.assertEqual(self.client.url_process.call_count, self.urls_file_lines)
            # Аргумент последнего вызова
            self.assertEqual(self.client.url_process.call_args[0][0], "http://www.google.com.au\n")


if __name__ == "__main__":
    unittest.main(exit=False)
