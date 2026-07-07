from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25565))
sock.send(b"46\n")
sock.close()