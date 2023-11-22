import asyncio
import argparse
from pathlib import Path
import aiohttp


DIR = "./www"


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


async def fetch_url(session, url, stats):
    try:
        async with session.get(url, timeout=10) as response:
            if __name__ == "__main__":
                print(f"{url} status: {response.status}")
            if response.status == 200:
                stats.add_good()
                return await response.text()
            stats.add_bad()
            return f"Error: {response.status}"
    except asyncio.TimeoutError:
        return "Error: Timeout"


async def fetch_urls(urls, concurrent_requests, stats):
    if concurrent_requests < 1:
        concurrent_requests = 1
        print("Concurrent requests value changed to 1")
    asyncio.get_event_loop()
    async with aiohttp.ClientSession() as session:

        tasks = []
        semaphore = asyncio.Semaphore(concurrent_requests)

        for url in urls:
            # Use semaphore to limit the concurrent requests
            async with semaphore:
                tasks.append(asyncio.ensure_future(fetch_url(session, url, stats)))

        return await asyncio.gather(*tasks)


def read_urls_list(urls_file):
    with open(urls_file, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file]
    return urls


def save_results(save_dir, urls, results):
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    for url, result in zip(urls, results):
        urlc = url
        for expr_subst in (
            ("http://", ""),
            ("https://", ""),
            ("/", ""),
            ("www.", ""),
        ):
            urlc = urlc.replace(*expr_subst)
        urlc = f"{save_dir}/{urlc}.html"
        with open(urlc, "w", encoding="utf-8") as file:
            file.write(f"URL: {url}\nResponse: {result}\n\n")


def get_data(urls, concurrent_requests, stats):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_urls(urls, concurrent_requests, stats))


def main():
    parser = argparse.ArgumentParser(description="Asynchronous URL fetcher")
    parser.add_argument("concurrent_requests", type=int, help="number of concurrent requests")
    parser.add_argument("urls_file", type=str, help="file containing list of URLs")

    args = parser.parse_args()
    concurrent_requests = args.concurrent_requests
    if concurrent_requests < 1:
        print(f"Invalid number of concurrent requests: {concurrent_requests}." " Should be positive integer.")
        return
    urls_file = args.urls_file

    stats = Info()
    urls = read_urls_list(urls_file)
    get_data(urls, concurrent_requests, stats)
    # save_results(DIR, urls, results)
    print(f"Good: {stats.get_good()}\nBad: {stats.get_bad()}\nTotal: {stats.get_total()}\n")


if __name__ == "__main__":
    main()
