import socket
import unittest.mock
from unittest.mock import Mock, call
import signal
from server import ServerApp
from client import ClientApp
from TimeoutException import TimeoutException


class ServerArgs:
    def __init__(self, workers, top_words):
        self.workers = workers
        self.top_words = top_words


class ClientArgs:
    def __init__(self, threads_count, path_to_urls):
        self.threads_count = threads_count
        self.path_to_urls = path_to_urls


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.args = ServerArgs(10, 5)
        self.app = ServerApp(self.args, 5)

    def test_parse_url(self):
        res = self.app.parse_url("qwerty")
        self.assertEqual(res, None)
        res = self.app.parse_url("http://qwerty")
        self.assertEqual(res, None)

    @unittest.mock.patch("re.findall")
    def test_get_most_frequent_words(self, findall_mock):
        findall_mock.return_value = []
        self.assertEqual(self.app.get_most_frequent_words("ababa"), "{}")
        findall_mock.return_value = ["abc", "bca", "bca", "cba", "abc", "abc"]
        self.args = ServerArgs(3, 2)
        self.app = ServerApp(self.args, 5)
        self.assertEqual(
            self.app.get_most_frequent_words("ababa"), '{"abc": 3, "bca": 2}'
        )

    @staticmethod
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    def test_process_request(self):
        # case 1: the function was fully executed
        self.app.parse_url = Mock()
        self.app.get_most_frequent_words = Mock()
        self.app.parse_url.return_value = "abcdeg"
        self.app.get_most_frequent_words.return_value = "{'a': 8, 'b': 5}"
        mock = Mock()
        self.app.jobs_queue.put(mock)
        self.app.processed_urls_count = 0

        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(1)
        try:
            self.app.process_request(self.app.jobs_queue)
        except TimeoutException:
            pass
        expected_calls = [
            call.recv(1024),
            call.recv().decode(),
            call.sendall(b"{'a': 8, 'b': 5}"),
            call.close(),
        ]
        self.assertEqual(mock.mock_calls, expected_calls)
        self.assertEqual(self.app.processed_urls_count, 1)
        self.assertTrue(self.app.parse_url.called)
        self.assertTrue(self.app.get_most_frequent_words.called)
        # case 2: the function parse_url returned None
        self.app.parse_url = Mock()
        self.app.get_most_frequent_words = Mock()
        self.app.parse_url.return_value = None
        mock = Mock()
        self.app.jobs_queue.put(mock)
        signal.alarm(1)
        try:
            self.app.process_request(self.app.jobs_queue)
        except TimeoutException:
            pass
        expected_calls = [call.recv(1024), call.recv().decode(), call.close()]
        self.assertEqual(mock.mock_calls, expected_calls)
        self.assertEqual(self.app.processed_urls_count, 1)
        self.assertTrue(self.app.parse_url.called)
        self.assertFalse(self.app.get_most_frequent_words.called)
        # case 3: the received data is None
        self.app.parse_url = Mock()
        self.app.get_most_frequent_words = Mock()
        self.app.parse_url.return_value = "qwerty"
        mock = Mock()
        mock.recv.return_value = None
        self.app.jobs_queue.put(mock)
        signal.alarm(1)
        try:
            self.app.process_request(self.app.jobs_queue)
        except TimeoutException:
            pass
        expected_calls = [call.recv(1024), call.close()]
        self.assertEqual(mock.mock_calls, expected_calls)
        self.assertEqual(self.app.processed_urls_count, 1)
        self.assertFalse(self.app.parse_url.called)
        self.assertFalse(self.app.get_most_frequent_words.called)

    def test_listen_port(self):
        # test binding
        host, port = "", 50007
        with socket.socket() as f:
            f.bind((host, port))
            self.assertEqual(self.app.listen_port(), 1)

    @unittest.mock.patch("socket.socket")
    def test_listen_port2(self, socket_mock):
        # test calls
        socket_inst_mock = socket_mock.return_value.__enter__.return_value
        socket_inst_mock.accept.return_value = (Mock(), "")
        self.app.lock = Mock()
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(1)
        try:
            self.app.listen_port()
        except TimeoutException:
            pass
        self.assertEqual(self.app.jobs_queue.qsize(), self.app.args.workers)
        self.assertEqual(socket_inst_mock.bind.call_count, 1)
        self.assertEqual(socket_inst_mock.listen.call_count, 1)
        self.assertEqual(socket_inst_mock.accept.call_count,
                         self.app.args.workers + 1)
        self.assertEqual(self.app.lock.acquire.call_count,
                         self.app.args.workers + 1)
        self.assertEqual(self.app.lock.release.call_count,
                         self.app.args.workers + 1)


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.args = ClientArgs(3, "./urls.json")
        self.app = ClientApp(self.args)

    def test_fill_urls_queue(self):
        # case1
        self.app.urls = ["a", "b", "c"]
        self.app.fill_urls_queue()
        result = []
        for _ in range(self.app.urls_queue.qsize()):
            result.append(self.app.urls_queue.get())
        self.assertEqual(result, ["a", "b", "c", None, None, None])
        # case2
        self.args = ClientArgs(1, "./urls.json")
        self.app = ClientApp(self.args)
        self.app.urls = []
        self.app.fill_urls_queue()
        result = []
        for _ in range(self.app.urls_queue.qsize()):
            result.append(self.app.urls_queue.get())
        self.assertEqual(result, [None])

    @unittest.mock.patch("socket.socket")
    def test_make_request(self, socket_mock):
        # case 1
        self.app.urls = []
        self.app.fill_urls_queue()
        self.app.make_request("", 50007)
        socket_inst_mock = socket_mock.return_value.__enter__.return_value
        self.assertEqual(socket_inst_mock.connect.call_count, 0)
        self.assertEqual(socket_inst_mock.sendall.call_count, 0)
        self.assertEqual(socket_inst_mock.recv.call_count, 0)
        self.assertEqual(socket_inst_mock.recv.return_value.decode.call_count, 0)
        # case 2
        self.app = ClientApp(self.args)
        self.app.urls = ["a", "b", "c", "d"]
        self.app.fill_urls_queue()
        self.app.make_request("", 50007)
        socket_inst_mock = socket_mock.return_value.__enter__.return_value
        self.assertEqual(socket_inst_mock.connect.call_count, 4)
        self.assertEqual(socket_inst_mock.sendall.call_count, 4)
        self.assertEqual(socket_inst_mock.recv.call_count, 4)
        self.assertEqual(socket_inst_mock.recv.return_value.decode.call_count, 4)


if __name__ == "__main__":
    unittest.main()
