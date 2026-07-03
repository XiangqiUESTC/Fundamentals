from socket import *
import time

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25565))

while True:
    start_time = time.time()
    sock.send(b'36')
    resp = sock.recv(1024)
    end_time = time.time()
    print(end_time - start_time)