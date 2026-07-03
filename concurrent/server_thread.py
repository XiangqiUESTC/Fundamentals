from socket import *
from threading import Thread
from fib import fib

def server():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(('localhost', 25565))
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("connected from", addr)
        thread = Thread(target=fib_handler, args=(client,), daemon=True)
        thread.start()

def fib_handler(client):
    while True:
        reqs = client.recv(1024)
        if not reqs:
            break
        n = int(reqs.decode())
        resp = str(fib(n)).encode("ascii") + b"\n"
        client.send(resp)
    print("thread finished")

server()