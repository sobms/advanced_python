import asyncio
import aiohttp
import bs4
from bs4 import BeautifulSoup, SoupStrainer
import json


async def parse(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            return html

def get_links_from_page(list_links, html):
    if len(list_links) == 100:
        return
    base_url = 'https://ru.wikipedia.org'
    soup = BeautifulSoup(html, 'lxml', parse_only=SoupStrainer('a'))
    for tag in soup:
        if isinstance(tag, bs4.element.Tag):
            if tag.has_key('href'):
                if 'http' in tag.get('href'):
                    list_links.append(tag.get('href'))
                elif tag.get('href').startswith('/'):
                    list_links.append(base_url+tag.get('href'))


if __name__ == '__main__':
    start_url = 'https://ru.wikipedia.org/wiki/TCP/IP'
    links_list = []
    loop = asyncio.get_event_loop()
    html = loop.run_until_complete(parse(start_url))
    get_links_from_page(links_list, html)
    data = {'link': links_list}
    print(len(links_list))
    json.dump(data, open('urls.json', 'w'))

