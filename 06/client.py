import socket
import threading
import argparse
from queue import Queue


TCPPORT = 12345
ENDMARK = "EOF"


class Client:
    server_ok = True

    def __init__(self, target_address):
        self.target_address = target_address
        self.urls_queue = Queue()

    def send_request(self):
        while self.server_ok:
            try:
                url = self.urls_queue.get(timeout=2)
                sock = socket.socket()
                sock.connect((self.target_address, TCPPORT))
                sock.sendall(url.encode())
                if url != ENDMARK:
                    data = sock.recv(1024)
                    print(f"{url.rstrip()}: {data.decode()}")
                else:
                    self.server_ok = False
            except ConnectionRefusedError:
                print(f"Server not listening port {TCPPORT}")
                self.server_ok = False
            except Exception:  # pylint: disable=broad-except
                pass

    def read_urls_from_file(self, urls_file):
        with open(urls_file, "r", encoding="utf-8") as file:
            for url in file:
                self.urls_queue.put(url)
        self.urls_queue.put(ENDMARK)  # End mark

    def start_threads(self, num_threads):
        threads = [
            threading.Thread(
                target=self.send_request, name=f"feeder_{thread_num}"
            )
            for thread_num in range(num_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client process.")
    parser.add_argument(dest="urls_file", type=str)
    parser.add_argument(dest="threads", type=int)

    ns = parser.parse_args()
    client = Client(target_address="localhost")
    client.read_urls_from_file(ns.urls_file)
    client.start_threads(ns.threads)
