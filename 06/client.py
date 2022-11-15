import socket
import argparse
import threading
import json
import queue
import os


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "threads_count",
        type=int,
        help="Specify threads count for client"
    )
    parser.add_argument(
        "path_to_urls",
        type=str,
        help="Specify path to file with urls")
    return parser.parse_args()


class ClientApp:
    def __init__(self, args):
        self.args = args
        with open(args.path_to_urls, "r") as f:
            self.urls = json.load(f)["links"]
        self.urls_queue = queue.Queue()

    def start(self):
        self.run_jobs()

    def fill_urls_queue(self):
        for link in self.urls:
            self.urls_queue.put(link)
        for _ in range(self.args.threads_count):
            self.urls_queue.put(None)

    def run_jobs(self):
        self.fill_urls_queue()
        host, port = "", 50007
        threads = [
            threading.Thread(target=self.make_request, args=(host, port))
            for _ in range(self.args.threads_count)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

    def make_request(self, host, port):
        while True:
            url = self.urls_queue.get()
            if url is None:
                break
            if socket.has_dualstack_ipv6():
                family = socket.AF_INET6
            else:
                family = socket.AF_INET
            with socket.socket(family=family) as s:
                s.connect((host, port))
                s.sendall(url.encode())
                response = s.recv(1024)
                print(response.decode())


if __name__ == "__main__":
    arguments = parse_arguments()
    if not os.path.isfile(arguments.path_to_urls):
        print(f"FileNotFoundError: file {arguments.path_to_urls} not exist.")
    else:
        app = ClientApp(arguments)
        app.start()
