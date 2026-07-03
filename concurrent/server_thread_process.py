from socket import *
from threading import Thread
from fib import fib
from concurrent.futures import ProcessPoolExecutor

pool = ProcessPoolExecutor(max_workers=4)

def server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("connected from", addr)
        thread = Thread(target=fib_handler, args=(client,), daemon=True)
        thread.start()


def fib_handler(client):
    while True:
        req = client.recv(1024)
        if not req:
            break
        n = int(req.decode())
        future = pool.submit(fib, n)
        rsp = future.result()
        client.send(str(rsp).encode("ascii") + b"\n")
    print("closed")

if __name__ == '__main__':
    server(("localhost", 25565))