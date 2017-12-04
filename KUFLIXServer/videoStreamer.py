import socket
import cv2
import pickle
import threading, time
import sys, socket
from ServerWorker import ServerWorker

class videoStreamer(object):
    def __init__(self):
        # connect to main server as agent
        HOST = ""
        PORT = 7900
        self.conNum = 0

        self.mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mainSock.connect((HOST, PORT))

        print("Connected to MainServer.")

        # get RTSP port from client
        self.portNum = self.mainSock.recv(1024)
        self.portNum = pickle.loads(self.portNum)
        print("Agent Port Num set : ", self.portNum)

        #start main listener
        threading._start_new_thread(self.checkAvailable, ())

        # for RTSP communication
        SERVER_PORT = int(self.portNum[1])
        self.agentSeqNum = SERVER_PORT - 12000

        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind(('', SERVER_PORT))
        rtspSocket.listen(3)

        print("AgentReady")

        while True:
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()
            self.conNum += 1

            if self.conNum >= 3:    ## 1 is unavailable
                self.mainSock.send(pickle.dumps("1"))
            else:
                self.mainSock.send(pickle.dumps("2"))
                # send to mainserver i'm unavailable
            print("Connected by", clientInfo['rtspSocket'])
            print("Connection num", self.conNum)

            ServerWorker(clientInfo, self.mainSock, self.agentSeqNum).run()

    def checkAvailable(self):
        while True:
            command = self.mainSock.recv(64)
            try:
                command = pickle.loads(command)
            except EOFError as e:
                continue
            if command == "out":
                print("client out")
                self.conNum -= 1

            time.sleep(60)