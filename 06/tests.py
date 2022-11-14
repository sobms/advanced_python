import socket

from server import ServerApp
from client import ClientApp
import unittest
import unittest.mock
from unittest.mock import Mock, call
import signal

class Server_args:
    def __init__(self, workers, top_words):
        self.workers = workers
        self.top_words = top_words

class ServerTest(unittest.TestCase):
    def setUp(self):
        self.args = Server_args(10, 5)
        self.app = ServerApp(self.args, 5)

    def test_parse_url(self):
        res = self.app.parse_url("qwerty")
        self.assertEqual(res, None)
        res = self.app.parse_url("http://qwerty")
        self.assertEqual(res, None)

    @unittest.mock.patch("re.findall")
    def test_get_most_frequent_words(self, findall_mock):
        findall_mock.return_value = []
        self.assertEqual(self.app.get_most_frequent_words("ababa"), '{}')
        findall_mock.return_value = ['abc', 'bca', 'bca', 'cba', 'abc', 'abc']
        self.args = Server_args(3, 2)
        self.app = ServerApp(self.args, 5)
        self.assertEqual(self.app.get_most_frequent_words("ababa"), '{"abc": 3, "bca": 2}')

    @staticmethod
    def signal_handler(signum, frame):
        raise Exception("Timed out!")

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
        except Exception:
            pass
        expected_calls = [call.recv(1024), call.recv().decode(),
                        call.sendall(b"{'a': 8, 'b': 5}"), call.close()]
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
        except Exception:
            pass
        expected_calls = [call.recv(1024), call.recv().decode(),
                        call.close()]
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
        except Exception:
            pass
        expected_calls = [call.recv(1024), call.close()]
        self.assertEqual(mock.mock_calls, expected_calls)
        self.assertEqual(self.app.processed_urls_count, 1)
        self.assertFalse(self.app.parse_url.called)
        self.assertFalse(self.app.get_most_frequent_words.called)

    def test_listen_port(self):
        host, port = "", 50007
        with socket.socket() as f:
            f.bind((host, port))
            self.assertEqual(self.app.listen_port(), 1)

class ClientTest(unittest.TestCase):
    pass

if __name__ == "__main__":
    #where should exception of url parsing process
    unittest.main()