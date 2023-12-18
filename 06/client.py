# client.py

import socket
import threading
import argparse
from queue import Queue
import time


DEFAULT_TCPPORT = 12345
ENDMARK = "EOF"
MAX_Q = 32
BUFF = 1024


class Client:
    server_ok = True
    show_output = True

    def __init__(self, target_address, urls_file, workers):
        self.th_count = 0
        self.urls_queue = Queue(MAX_Q)
        self.urls_file = urls_file
        self.workers = workers
        assert workers > 0
        pos = target_address.find(":")
        if pos == -1:
            self.tcp_port, self.target_address = DEFAULT_TCPPORT, target_address
        else:
            self.tcp_port, self.target_address = (
                int(target_address[pos + 1 :]),
                target_address[:pos],
            )

    def send_request(self):
        sock = socket.socket()
        while self.server_ok:
            try:
                url = self.urls_queue.get(timeout=2)
                sock = socket.socket()
                sock.connect((self.target_address, self.tcp_port))
                sock.sendall(url.encode())
                if url != ENDMARK:
                    data = sock.recv(BUFF)
                    if self.show_output:
                        print(f"{url.rstrip()}: {data.decode()}")
                else:
                    self.server_ok = False
            except ConnectionRefusedError:
                print(f"Server not listening port {self.tcp_port}")
                self.server_ok = False
                return
                # raise Exception("An error occurred", "server not listening port", 42)
            except Exception:  # pylint: disable=broad-except
                pass
            finally:
                sock.close()

    def url_process(self, url):
        pass

    def read_urls_from_file(self):
        try:
            url = ""
            with open(self.urls_file, "r", encoding="utf-8") as file:
                for url in file:
                    self.url_process(url)
                    delay = 0.5
                    while self.urls_queue.full():
                        time.sleep(delay)
                        delay += 0.3
                    self.urls_queue.put(url)
            file.close()
        except FileNotFoundError as err:
            print(f"Cannot open file {self.urls_file}")
            print(f"{url} {type(err).__name__} was raised: {err}")
        finally:
            self.urls_queue.put(ENDMARK)  # End mark

    def start_threads(self):
        threads = [threading.Thread(target=self.send_request, name=f"feeder_{thread_num}") for thread_num in range(self.workers)]

        # Отдельный поток чтения URL из файла и помещения его в очередь
        threads.append(threading.Thread(target=self.read_urls_from_file, name="reader_0"))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            self.th_count += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client process.")
    parser.add_argument(dest="urls_file", type=str)
    parser.add_argument(dest="threads", type=int)

    ns = parser.parse_args()
    client = Client(target_address="localhost", urls_file=ns.urls_file, workers=ns.threads)
    client.start_threads()
