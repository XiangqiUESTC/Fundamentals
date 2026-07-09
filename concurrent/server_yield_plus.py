import select
from fib import fib
from concurrent.futures import ThreadPoolExecutor as Pool
from socket import *
from collections import deque
from select import select

pool = Pool(10)
tasks = deque()
recv_wait = {}
send_wait = {}

def server(addr):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(5)
    while True:
        # need wait socket
        yield "recv", sock
        client, addr = sock.accept()
        print(f"Connected from {addr}" )
        tasks.append(fib_handler(client))



def fib_handler(client):
    while True:
        yield "recv", client
        req = client.recv(1024)
        if not req:
            break
        n = int(req.decode("ascii"))
        # need wait cpu
        future = pool.submit(fib, n)
        res = future.result()
        yield "send", client
        client.send(str(res).encode("ascii")+b"\n")
    client.close()

def run():
    while any([recv_wait, send_wait, tasks]):
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
                continue
        else:
            can_recv, can_send , [] = select(recv_wait, send_wait, [])
            for x in can_recv:
                tasks.append(recv_wait.pop(x))
            for x in can_send:
                tasks.append(send_wait.pop(x))



tasks.append(server(("localhost", 25565)))
run()