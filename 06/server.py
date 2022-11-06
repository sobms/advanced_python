import argparse
import socket
import queue
import threading

def parse_url(que):
    url, conn = que.get()
    conn.sendall(url)
    lock = threading.Lock()
    lock.acquire()
    global processed_urls_count
    processed_urls_count += 1
    print("="*30)
    print(f"Count of processed urls: {processed_urls_count}")
    print("=" * 30)
    lock.release()
    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", required=True, type=int,
                        help="specify number of workers")
    parser.add_argument("-k", "--top_words", required=True, type=int,
                        help="specify count of most frequent words")
    args = parser.parse_args()
    que = queue.Queue(args.workers)
    global processed_urls_count
    processed_urls_count = 0
    #init and run workers
    threads = [
        threading.Thread(target=parse_url,
                         args=(que,))
        for _ in range(args.workers)
    ]
    for th in threads:
        th.start()
    #create tcp socket and start listening of port
    host, port = "", 50007  # all interfaces, port 8080
    if socket.has_dualstack_ipv6():
        family = socket.AF_INET6
    else:
        family = socket.AF_INET
    with socket.socket(family=family) as s:
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            print('Connected by', addr)
            data = conn.recv(1024)
            print(int.from_bytes(data, "big"))
            que.put((data, conn))
            #master не должен закрывать соединение по этому порту пока не отдаст результат -> это мешает распараллеливанию
            #как вернуть информацию о том сколько урлов обработано, т е сколько воркеров выполнилось



