import socket
import errno
import os
import threading
import argparse
from queue import Queue
from html.parser import HTMLParser
from collections import Counter
from urllib.request import urlopen
from nltk.tokenize import RegexpTokenizer
import psutil

TCPPORT = 12345
ENDMARK = "EOF"


def read_url(url):
    with urlopen(url, timeout=10) as data:
        return data.read().decode()


class HtmlParser(HTMLParser):
    # lock = threading.Semaphore(4)
    lock = threading.Lock()

    def __init__(self, k_top, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curr_tag = ""
        self.k_top = k_top
        self.tokenizer = RegexpTokenizer(r"\w+")
        self.total_calls = 0
        self.words = []

    def error(self, message):
        pass

    def feed(self, data):
        self.words = []
        with self.lock:
            super().feed(data)
            self.total_calls += 1

    def get_total(self):
        return self.total_calls

    def handle_starttag(self, tag, attrs):
        self.curr_tag = tag

    def handle_data(self, data):
        skip_tags = ["script", "meta", "img", "style", "nav", "menu"]
        if self.curr_tag not in skip_tags:
            self.words.extend(self.tokenizer.tokenize(data))

    def most_common_words(self):
        return dict(Counter(self.words).most_common(self.k_top))


def process_requests(tasks, parser):
    while threading.active_count() > 1:
        try:
            url, client = tasks.get(timeout=5)
            if url == ENDMARK:
                tasks.put((url, client))
                print(f"Stop process_requests {threading.current_thread().name}")
                break
            try:
                parser.feed(read_url(url))
                most_common_words = parser.most_common_words()
                client.send(str(most_common_words).encode())
                print(f"Total URLs processed: {parser.get_total()}")
            except Exception as err:  # pylint: disable=broad-except
                answer_to_client = "Error: URL could not be processed".encode()
                client.send(answer_to_client)
                print(f"{url} {type(err).__name__} was raised: {err}")
        except Exception:  # pylint: disable=broad-except
            pass


def master_server(tasks_queue):
    sock = socket.socket()
    try:
        sock.bind(("localhost", TCPPORT))
    except socket.error as err:
        if err.errno == errno.EADDRINUSE:
            print(f"Port {TCPPORT} is already in use")
        else:
            print(err)
        current_pid = os.getpid()
        process = psutil.Process(current_pid)
        process.terminate()

    sock.listen(5)
    try:
        while True:
            if threading.active_count() == 1:
                break
            client, _ = sock.accept()
            tasks_queue.put((client.recv(1024).decode(), client))
            sock.settimeout(10.0)  # Without timeout we have to send another line to finish loop
    except KeyboardInterrupt:
        current_system_pid = os.getpid()
        this_system = psutil.Process(current_system_pid)
        this_system.terminate()
    except socket.timeout:
        if threading.active_count() == 1:
            print("Done: master_server finished")
    finally:
        sock.close()


def start_workers(worker_count, parser):
    tasks_queue = Queue()
    threads = [
        threading.Thread(
            target=process_requests,
            args=(tasks_queue, parser),
        )
        for _ in range(worker_count)
    ]
    for thread in threads:
        thread.start()

    master_server(tasks_queue)

    for thread in threads:
        thread.join()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", dest="workers", type=int, required=True)
    parser.add_argument("-k", dest="k_top", type=int, required=True)
    return parser


if __name__ == "__main__":
    arg_parser = parse_arguments()
    ns = arg_parser.parse_args()
    custom_parser = HtmlParser(ns.k_top)
    start_workers(ns.workers, custom_parser)
