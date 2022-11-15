import json
import asyncio
import aiohttp
import bs4
from bs4 import BeautifulSoup, SoupStrainer


async def parse(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.text()
            return response


def get_links_from_page(list_links, html):
    if len(list_links) == 100:
        return
    base_url = "https://ru.wikipedia.org"
    soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer("a"))
    for tag in soup:
        if isinstance(tag, bs4.element.Tag):
            if "href" in tag:
                if "http" in tag.get("href"):
                    list_links.append(tag.get("href"))
                elif tag.get("href").startswith("/"):
                    list_links.append(base_url + tag.get("href"))


if __name__ == "__main__":
    START_URL = "https://ru.wikipedia.org/wiki/TCP/IP"
    links_list = []
    loop = asyncio.get_event_loop()
    html_page = loop.run_until_complete(parse(START_URL))
    get_links_from_page(links_list, html_page)
    data = {"link": links_list}
    print(len(links_list))
    with open("urls.json", "w") as f:
        json.dump(data, f)
