import unittest
import asyncio
from unittest.mock import AsyncMock, Mock, call, MagicMock
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
from fetcher import Fetcher


class FetcherTestCase(AioHTTPTestCase):
    def setUp(self):
        urls = [
            "https://ru.wikipedia.org/wiki/Transmission_Control_Protocol"
            for _ in range(100)
        ]
        self.fetcher = Fetcher(urls, 5, 5)

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        async def hello():
            return web.Response(text="Hello, world")

        app = web.Application()
        app.router.add_get("/", hello)
        return app

    def test_start_session(self):
        self.fetcher.que = AsyncMock()
        self.fetcher.process_urls = AsyncMock()
        asyncio.create_task = Mock()
        self.fetcher.run()
        # test queue
        expected_calls = [call(url) for url in self.fetcher.urls]
        self.assertEqual(expected_calls, self.fetcher.que.put.mock_calls)
        self.assertTrue(self.fetcher.que.join.called)
        # test process_urls() calls count
        self.assertEqual(
            self.fetcher.process_urls.call_count,
            self.fetcher.tasks_count
        )
        # test count of tasks and canceling tasks
        self.assertEqual(
            asyncio.create_task.call_count,
            self.fetcher.tasks_count
        )
        self.assertEqual(
            asyncio.create_task.return_value.cancel.call_count,
            self.fetcher.tasks_count
        )

    def test_get_most_frequent_words(self):
        self.fetcher.top_words = 2
        self.assertEqual(
            self.fetcher.get_most_frequent_words(
                "aba bab aba aab aab"
            ),
            '{"aba": 2, "aab": 2}',
        )
        self.assertEqual(self.fetcher.get_most_frequent_words(""), "{}")
        self.assertEqual(
            self.fetcher.get_most_frequent_words(
                "ase: aec. alm! alm! Ase alm, aec."
            ),
            '{"alm": 3, "aec": 2}',
        )

    async def test_process_urls(self):
        # fill queue
        urls = ["url1", "url2", "url3", "url4"]
        for url in urls:
            await self.fetcher.que.put(url)
        response_texts = [
            "ase: aec. alm! alm! Ase alm, aec.",
            "aba .bab aba abc",
            "qwerty!! qwe... ewq... qwerty.",
            "qwr., qwr, qwr",
        ]
        # mock client session
        session = MagicMock()
        # mock session.get function()
        session.get = MagicMock()
        session.get.return_value.__aenter__.return_value.text.side_effect = (
            response_texts
        )
        # mock get_most_frequent_words() function
        self.fetcher.get_most_frequent_words = Mock()
        # run process_urls() function
        task = asyncio.create_task(self.fetcher.process_urls(session))
        await self.fetcher.que.join()
        task.cancel()
        # check that session.get() function was called with necessary urls
        session.get.assert_has_calls(
            [call(url) for url in urls],
            any_order=True
        )
        # check that get_most_frequent_words() got correct texts
        self.fetcher.get_most_frequent_words.assert_has_calls(
            [call(text) for text in response_texts]
        )


if __name__ == "__main__":
    unittest.main()
