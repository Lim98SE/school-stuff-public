import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 25967

server.bind(("localhost", port))

server.listen(32)