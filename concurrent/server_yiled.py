from hmac import new

from fib import fib
from socket import *
from collections import deque
from select import select

tasks  = deque()
recv_wait = {}
send_wait = {}

def run():
    while any([tasks, recv_wait, send_wait]):
        if tasks:
            task = tasks.popleft()
            try:
                why, what = next(task)
                if why == "recv":
                    recv_wait[what] = task
                elif why == "send":
                    send_wait[what] = task
                else:
                    raise RuntimeError("Fuck!")
            except StopIteration:
                pass
        else:
            can_recv, can_send, [] = select(recv_wait, send_wait, [])

            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))



def server(addr):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(5)
    while True:
        yield "recv", sock
        client, addr = sock.accept() # block
        task = fib_handler(client)
        tasks.append(task)

def fib_handler(client):
    while True:
        yield "recv", client
        req = client.recv(1024) # block
        if not req:
            break
        else:
            n = int(req.decode("ascii"))
            result = fib(n)
            yield "send", client
            client.send(str(result).encode("ascii") + b"\n") # block
    print("closing client")
    client.close()

tasks.append(server(("localhost", 25565)))
run()
