from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25565))

n = 0

from threading import Thread

def monitor():
    global n
    while True:
        time.sleep(1)
        print(n)
        n = 0

thread = Thread(target=monitor, daemon=True).start()

while True:
    sock.send(b'1')
    resp = sock.recv(1024)
    n += 1
