from socket import *
from fib import fib

def server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind(address)
    sock.listen(2)

    while True:
        client, addr = sock.accept() # block，等待建立tcp连接
        print('Client connected from', addr)
        fib_handler(client)

def fib_handler(client):
    while True:
        req = client.recv(1024) # block，等待客户端发送消息
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode("ascii") + b'\n'
        client.send(resp) # block
    client.send(b"hhhhhhh")
    print('Client disconnected')

server(("", 25565))