from collections import Counter
import asyncio
import json
import re
import argparse
import time
import aiohttp
import ijson
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "tasks",
        type=int,
        help="specify number of simultaneous requests"
    )
    parser.add_argument(
        "top_words",
        type=int,
        help="specify count of most frequent words",
    )
    parser.add_argument(
        "path_to_urls",
        type=str,
        help="Specify path to file with urls"
    )

    return parser.parse_args()


class Fetcher:
    def __init__(self, urls, tasks_count, top_words):
        self.urls = urls
        self.tasks_count = tasks_count
        self.top_words = top_words
        self.que = asyncio.Queue()

    def set_urls(self, urls):
        self.urls = urls

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_session())

    def get_most_frequent_words(self, html):
        soup = BeautifulSoup(html, "lxml")
        words = re.findall("[A-Za-zА-Яа-я0-9_]+", soup.text)
        top_words = Counter(words).most_common(self.top_words)
        return json.dumps(dict(top_words), ensure_ascii=False)

    async def process_urls(self, session):
        while True:
            url = await self.que.get()

            try:
                async with session.get(url) as resp:
                    response = await resp.text()
                    result = self.get_most_frequent_words(response)
                    print(result)
            except Exception as err:
                print(f"Worker catch error: {err}")
            finally:
                self.que.task_done()

    async def start_session(self):
        for url in self.urls:
            await self.que.put(url)

        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            tasks = [
                asyncio.create_task(self.process_urls(session))
                for _ in range(self.tasks_count)
            ]
            await self.que.join()
            end_time = time.time()
            print(
                f"Time of fetching with {self.tasks_count} tasks: "
                f"{end_time-start_time}"
            )
            for task in tasks:
                task.cancel()


def get_batch(file, batch_size=20):
    URLS = ijson.items(file, "links.item")
    batch = []
    for url in URLS:
        batch.append(url)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch


if __name__ == "__main__":
    args = parse_arguments()
    fetcher = Fetcher([], args.tasks, args.top_words)
    with open(args.path_to_urls, "r") as f:
        batch_size = 20
        for batch in get_batch(f, batch_size):
            fetcher.set_urls(batch)
            fetcher.run()
