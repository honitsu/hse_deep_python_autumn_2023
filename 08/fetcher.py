#!/usr/bin/env python3
# fetcher.py

import argparse
import asyncio
import aiofiles
import httpx

EOF = "EOF"


async def fetch_url(session, url):
    try:
        ret = await session.get(url)
        retval = (url, ret.status_code, ret.reason_phrase)
    except Exception:
        retval = (url, -1, "Error")
    return retval


async def read_urls_list(urls_file, queue):
    async with aiofiles.open(urls_file, "r", encoding="utf-8") as file:
        async for line in file:
            await queue.put(line.strip())
        await queue.put(EOF)


async def fetch_urls(session, queue):
    retval = []
    while True:
        url = await queue.get()
        if url == EOF:
            await queue.put(url)
            queue.task_done()
            break
        try:
            retval.append(tuple(await fetch_url(session, url)))
        except Exception:  # Перестраховка
            retval.append((url, -100, "Erron in fetch_url"))
        queue.task_done()
    return retval


async def get_data(urls_file, concurrent_requests):
    queue = asyncio.Queue(maxsize=concurrent_requests * 2)
    queue_task = asyncio.create_task(read_urls_list(urls_file, queue))

    async with httpx.AsyncClient() as session:
        tasks = [asyncio.create_task(fetch_urls(session, queue)) for _ in range(concurrent_requests)]

        await queue.join()
        await queue_task
        value = await asyncio.gather(*tasks)
        return value


async def start_fetchers(urls_file, workers):
    value = await get_data(urls_file, concurrent_requests=workers)
    plain_array = []
    # Convert array of arrays into single array
    for task_data in value:
        for val in task_data:
            plain_array.append(val)
    return plain_array


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description="Asynchronous URL fetcher")
    parser.add_argument("concurrent_requests", type=int, help="Number of concurrent requests")
    parser.add_argument("urls_file", type=str, help="File, containing list of URLs")
    args = parser.parse_args()
    workers = int(args.concurrent_requests)
    if workers < 1 or workers > 32000:
        print(f"Invalid number of concurrent requests: {workers}. Should be in range 1-32000")
        return
    ret = asyncio.run(start_fetchers(args.urls_file, workers))
    for tup in ret:
        print(tup)


if __name__ == "__main__":
    main()  # pragma: no cover
