import argparse
import socket
import queue
import threading
import re
from collections import Counter
import json
import requests
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--workers",
        required=True,
        type=int,
        help="specify number of workers"
    )
    parser.add_argument(
        "-k",
        "--top_words",
        required=True,
        type=int,
        help="specify count of most frequent words",
    )
    return parser.parse_args()


class ServerApp:
    def __init__(self, args, sem_count):
        self.lock = threading.RLock()
        self.processed_urls_count = 0
        self.args = args
        self.jobs_queue = queue.Queue(self.args.workers)
        self.semaphore = threading.Semaphore(sem_count)

    def start(self):
        self.run_workers()
        self.listen_port()

    @staticmethod
    def parse_url(url):
        try:
            with requests.Session() as s:
                response = s.get(url)
                return response.text
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"Some error occurred: {err}")
            return None

    def get_most_frequent_words(self, html):
        soup = BeautifulSoup(html, "lxml")
        words = re.findall("[A-Za-zА-Яа-я0-9_]+", soup.text)
        top_words = Counter(words).most_common(self.args.top_words)
        return json.dumps(dict(top_words), ensure_ascii=False)

    def process_request(self, que):
        while True:
            # try to get new client
            conn = que.get()
            data = conn.recv(1024)
            if data is None:
                conn.close()
                print("Received None")
                continue
            with self.semaphore:
                html = self.parse_url(data.decode())
            if html is None:
                conn.close()
                continue
            response_data = self.get_most_frequent_words(html)
            conn.sendall(response_data.encode())
            with self.lock:
                # to prevent race condition or simultaneous access to data
                self.processed_urls_count += 1
                print("=" * 30)
                print(f"Count of processed urls: {self.processed_urls_count}")
                print("=" * 30)
            conn.close()

    def run_workers(self):
        # init and run workers
        threads = [
            threading.Thread(target=self.process_request,
                             args=(self.jobs_queue,))
            for _ in range(self.args.workers)
        ]
        for th in threads:
            th.start()

    def listen_port(self):
        host, port = "", 50007  # all interfaces, port 50007
        if socket.has_dualstack_ipv6():
            family = socket.AF_INET6
        else:
            family = socket.AF_INET
        with socket.socket(family=family) as s:
            try:
                s.bind((host, port))
                s.listen(self.args.workers)
            except socket.error as msg:
                print("Socket binding error: " + str(msg))
                return 1
            while True:
                conn, addr = s.accept()
                self.lock.acquire()
                # to not write from different thread simultaneous
                print("Connected by", addr)
                self.lock.release()
                self.jobs_queue.put(conn)


if __name__ == "__main__":
    arguments = parse_arguments()
    app = ServerApp(arguments, 3)
    app.start()
