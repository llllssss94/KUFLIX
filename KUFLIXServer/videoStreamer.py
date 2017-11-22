import socket
import cv2

class videoStreamer(object):

    def streaming(self):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

        self.capture = cv2.VideoCapture("SampleVideo_1280x720_1mb.mp4")
        self.frameNum = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        print("number of frames", self.frameNum)

        data, self.clntAddr = self.sock.recvfrom(1024)
        data = data.decode("utf-8", "ignore")
        print(data)
        data = bin(self.frameNum)
        data = data.encode("utf-8")
        self.sock.sendto(data, self.clntAddr)

        self.sendFrame()

        self.sock.close()

    def sendFrame(self):

        for i in range(0, self.frameNum):
            ret, data = cv2.VideoCapture.read(self.capture)

            cv2.imwrite("./tmp/temp.png", data)

            f = open("./tmp/temp.png", "rb")

            data = f.read(1024)
            while(data):
                self.sock.sendto(data, self.clntAddr)
                data = f.read(1024)
            self.sock.sendto("EOF".encode("utf-8"), self.clntAddr)

            f.close()

if __name__ == "__main__":
    streamer = videoStreamer()
    streamer.streaming()