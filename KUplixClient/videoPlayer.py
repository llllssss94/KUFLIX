import socket
import cv2

class videoPlayer(object):

    def __init__(self, video_id = None):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005

        server_address = (UDP_IP, UDP_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = "hi"

        message = message.encode("utf-8")

        self.sock.sendto(message, server_address)

        data, address = self.sock.recvfrom(1024)

        data = data.decode("utf-8", "ignore")

        self.frameNum = int(data, 2)

        print("echo = ", self.frameNum)

        self.writer = cv2.VideoWriter("LiveStream.avi", cv2.VideoWriter_fourcc('D','I','V','X'), 20, (1280, 720))

    def requestFrame(self):

        f = open("./tmp/temp.png", "wb")

        data, address = self.sock.recvfrom(1024)
        while(data):
            f.write(data)
            data, address = self.sock.recvfrom(1024)
            if data == "EOF".encode("utf-8"):
                break
        f.close()

        frame = cv2.imread("./tmp/temp.png")

        self.writer.write(frame)

    def receiving(self):
        for i in range(0, self.frameNum):
            self.requestFrame()
        self.sock.close()

if __name__ == "__main__":
    player = videoPlayer()
    player.receiving()