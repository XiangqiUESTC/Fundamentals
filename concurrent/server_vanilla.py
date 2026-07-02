from socket import *


def server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = sock.accept() # block

