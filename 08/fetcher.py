import asyncio
import aiohttp
from bs4 import BeautifulSoup
from collections import Counter
import json
import re
import argparse
import time


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
        help="Specify path to file with urls")

    return parser.parse_args()

class Fetcher:
    def __init__(self, urls, tasks_count, top_words):
        self.urls = urls
        self.tasks_count = tasks_count
        self.top_words = top_words
        self.que = asyncio.Queue()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_session())

    def get_most_frequent_words(self, html):
        soup = BeautifulSoup(html, "lxml")
        words = re.findall("[A-Za-zА-Яа-я0-9_]+", soup.text)
        top_words = Counter(words).most_common(self.top_words)
        return json.dumps(dict(top_words), ensure_ascii=False)

    async def fetch_url(self, session):
        while True:
            url = await self.que.get()
            try:
                async with session.get(url) as resp:
                    response = await resp.text()
                    print(self.get_most_frequent_words(response))
            finally:
                self.que.task_done()

    async def start_session(self):
        for url in self.urls:
            await self.que.put(url)

        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            workers = [
                asyncio.create_task(self.fetch_url(session))
                for _ in range(self.tasks_count)
            ]
            await self.que.join()
            end_time = time.time()
            print(f"Time of fetching with {self.tasks_count} tasks: {end_time-start_time}")
            for worker in workers:
                worker.cancel()

if __name__ == '__main__':
    args = parse_arguments()
    with open(args.path_to_urls, 'r') as f:
        urls = json.load(f)["links"]
    fetcher = Fetcher(urls, args.tasks, args.top_words)
    fetcher.run()
