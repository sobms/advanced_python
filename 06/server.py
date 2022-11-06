import argparse
import socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", required=True, type=int,
                        help="specify number of workers")
    parser.add_argument("-k", "--top_words", required=True, type=int,
                        help="specify count of most frequent words")
    args = parser.parse_args()
    #create tcp socket
    host, port = "", 50007  # all interfaces, port 8080
    if socket.has_dualstack_ipv6():
        family = socket.AF_INET6
    else:
        family = socket.AF_INET
    with socket.socket(family=family) as s:
        s.bind((host, port))
        s.listen(1)

        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)



