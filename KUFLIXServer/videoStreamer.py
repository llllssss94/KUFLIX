import socket
import cv2
import pickle
import threading
import sys, socket

from ServerWorker import ServerWorker

class videoStreamer(object):
    def __init__(self):
        # connect to main server as agent
        HOST = ""
        PORT = 7900
        self.clntList = {}
        self.conNum = 0

        self.mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mainSock.connect((HOST, PORT))

        print("Connected to MainServer.")
        print("AgentReady")

        # get RTSP port from client
        self.portNum = self.mainSock.recv(1024)
        self.portNum = pickle.loads(self.portNum)

        # for RTSP communication
        SERVER_PORT = self.portNum

        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', SERVER_PORT))
        rtspSocket.listen(3)

        while True:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()
            self.conNum += 1

            if self.clntList.__len__() >= 3:
                print("full!")
                # send to mainserver i'm unavailable
            print("Connected by", clientInfo['rtspSocket'])

            ServerWorker(clientInfo).run()

    def commClient(self, clntSock):
        #first cilent send cid
        #and agent request to mainServer
        #next send to client to ready for streaming
        #wait cilent ready signal and signal came streaming start
        print("ASdsad")


    def streaming(self, portNum, seqNum, path):
        UDP_IP = "127.0.0.1"
        UDP_PORT = portNum + 10000

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        data, clntAddr = sock.recvfrom(1024)
        data = data.decode("utf-8", "ignore")
        print(data) ## It will be cid and agent ask to main server about path
        self.mainSock.send(pickle.dumps(data))

        self.capture = cv2.VideoCapture("SampleVideo_1280x720_30mb.mp4")
        self.frameNum = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        print("number of frames", self.frameNum)
        ## and get path and send to client it will ready

        data = bin(self.frameNum)
        data = data.encode("utf-8")
        sock.sendto(data, clntAddr)

        self.sendFrame(sock, clntAddr)

        self.clntList.pop(seqNum)
        sock.close()

    def sendFrame(self, sock, clntAddr):

        for i in range(0, self.frameNum):
            ret, data = cv2.VideoCapture.read(self.capture)


            cv2.imwrite("./tmp/temp.png", data)

            f = open("./tmp/temp.png", "rb")


            data = f.read(1024)
            while(data):
                sock.sendto(data, clntAddr)
                data = f.read(1024)
            sock.sendto("EOF".encode("utf-8"), clntAddr)

            f.close()

def startAgent():
    streamer = videoStreamer()

if __name__ == "__main__":
    streamer = videoStreamer()
    streamer.streaming()