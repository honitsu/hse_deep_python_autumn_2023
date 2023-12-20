# fetcher.py
import argparse
import asyncio
import aiofiles
import httpx

EOF = "EOF"


class Info:
    def __init__(self):
        self.__good = 0
        self.__bad = 0
        self.__total = 0

    def add_good(self):
        self.__good += 1
        self.add_total()

    def add_bad(self):
        self.__bad += 1
        self.add_total()

    def add_total(self):
        self.__total += 1

    def get_good(self):
        return self.__good

    def get_bad(self):
        return self.__bad

    def get_total(self):
        return self.__total

    def print(self):
        print(f"\nGood: {self.get_good()}\nBad: {self.get_bad()}\nTotal: {self.get_total()}\n")


def get_hostname(url):
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    url = url.replace("www.", "")
    return url


async def fetch_url(session, url, stats):
    ret = await session.get(url)
    if ret.status_code == 200:
        stats.add_good()
    else:
        stats.add_bad()
    if __name__ == "__main__":
        print(f"{get_hostname(url)[:30]:30s} {ret}")
    return ret


async def read_urls_list(urls_file, queue):
    async with aiofiles.open(urls_file, "r", encoding="utf-8") as file:
        async for line in file:
            await queue.put(line.strip())
        await queue.put(EOF)


async def fetch_urls(session, queue, queue_task, stats):
    while True:
        url = await queue.get()
        if url == EOF:
            await queue.put(url)
            queue.task_done()
            break
        await fetch_url(session, url, stats)
        queue.task_done()
    return


async def get_data(urls_file, concurrent_requests, stats):
    queue = asyncio.Queue(maxsize=concurrent_requests * 5)
    queue_task = asyncio.create_task(read_urls_list(urls_file, queue))

    async with httpx.AsyncClient() as session:
        tasks = [asyncio.create_task(fetch_urls(session, queue, queue_task, stats)) for _ in range(concurrent_requests)]

        await queue.join()
        await queue_task
        await asyncio.wait(tasks)


def start_fetchers(urls_file, workers):
    stats = Info()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(get_data(urls_file, concurrent_requests=workers, stats=stats))
    finally:
        loop.close()
    return stats


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description="Asynchronous URL fetcher")
    parser.add_argument("concurrent_requests", type=int, help="Number of concurrent requests")
    parser.add_argument("urls_file", type=str, help="File, containing list of URLs")
    args = parser.parse_args()
    workers = int(args.concurrent_requests)
    if workers < 1 or workers > 32000:
        print(f"Invalid number of concurrent requests: {workers}. Should be in range 1-32000")
        return
    stats = start_fetchers(args.urls_file, workers)
    stats.print()


if __name__ == "__main__":
    main()  # pragma: no cover
