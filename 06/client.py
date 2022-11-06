import socket
import argparse
import threading

def make_request(host, port):
    if socket.has_dualstack_ipv6():
        family = socket.AF_INET6
    else:
        family = socket.AF_INET

    with socket.socket(family=family) as s:
        s.connect((host, port))
        s.sendall((s.getsockname()[1]).to_bytes(2, byteorder='big'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('threads_count', type=int,
                        help='Specify threads count for client')
    parser.add_argument('path_to_urls', type=str,
                        help='Specify path to file with urls')
    args = parser.parse_args()
    host, port = "", 50007
    threads = [
        threading.Thread(target=make_request,
                         args=(host, port,))
        for _ in range(args.threads_count)
    ]
    for th in threads:
        th.start()

    # for th in threads:
    #     th.join()