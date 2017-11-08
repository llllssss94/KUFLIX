import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

server_address = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "hi"

message = message.encode("utf-8")

send = sock.sendto(message, server_address)

data, address = sock.recvfrom(1024)


data = data.decode("utf-8", "ignore")

data = int(data, 2)

print("echo = ", data)

data, address = sock.recvfrom(1024)

data = data.decode("utf-8", "ignore")

f = open(data, "wb")

data, address = sock.recvfrom(1024)

while(data):
    f.write(data)
    data, address = sock.recvfrom(1024)
f.close()
sock.close()