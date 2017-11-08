import socket
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

capture = cv2.VideoCapture("SampleVideo_1280x720_1mb.mp4")

frameNum = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

print("number of frames", frameNum)

data, clntAddr = sock.recvfrom(1024)

data = data.decode("utf-8", "ignore")

print(data)

data = bin(frameNum)

data = data.encode("utf-8")

sock.sendto(data, clntAddr)

data = "test.png"

data = data.encode("utf-8")

sock.sendto(data, clntAddr)

ret, data = cv2.VideoCapture.read(capture)

cv2.imwrite("test.png", data)

f = open("test.png", "rb")

data = f.read(1024)
while(data):
    sock.sendto(data, clntAddr)
    data = f.read(1024)

f.close()
sock.close()