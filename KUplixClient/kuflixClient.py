import socket
import threading

class kuflixClient(object):
    def __init__(self):
        self.uid = None
        self.id = None
        self.name = None
        self.rank = None
        self.tmList = {}

    def protocolGenerator(self, mode = 0, type = 0, msgList = []):
        if mode == 0:   #login mode
            if type == 0:  # login protocol ##msgtype | id | hashed_passward
                msg = "00" + "," + msgList[0] + "," + msgList[1]
                return msg
            else:  # join protocol ##msgtype | id | hashed_passward | name | age
                msg = "01" + "," + msgList[0] + "," + msgList[1] + "," + msgList[2] + "," + msgList[3]
                return msg
        else:   #main mode
            if type == 0:  # 00 ##[00 | LABEL | UID]
                msg = "00" + "," + msgList[0] + "," + msgList[1]
                return msg
            elif type == 1:  # 01 ##[01 | LABEL | UID]
                msg = "01" + "," + msgList[0] + "," + msgList[1]
                return msg
            elif type == 2:  # 10 ##[10 | MESSAGE | UID]
                msg = "10" + "," + msgList[0] + "," + msgList[1]
                return msg
            else:  # 11 ##[11 | VIDEO_ID | UID]
                msg = "11" + "," + msgList[0] + "," + msgList[1]
                return msg


    def loginRequest(self, msg):
        HOST = "127.0.0.1"
        PORT = 8080

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        s.send(bytes(msg,"utf-8"))

        data = s.recv(1024)

        data = data.decode("utf-8", "ignore")

        msgList = data.split(",")

        if msgList[0] == "00":
            port = msgList[1]
            if port == "0000":
                #login fail
                print("login failed")
            else:
                self.uid = msgList[2]   #save uid
                print("uid : ", self.uid , "port : ", port)
                self.mainLoop(port)

        else:
            flag = msgList[1]
            if flag == "0":
                print("fail")
            else:
                print("success")
        s.close()

        #Through return value, system signal to GUIhandler what has to be

    def mainLoop(self, port):
        HOST = "127.0.0.1"
        PORT = 8100  # port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        msg = self.sock.recv(1024)
        print("uid request")
        if msg.decode("utf-8", "ignore") == "uid":
            self.sock.send(bytes(self.uid, "utf-8"))
            print("send")

        self.setUp(self.sock)

    def listener(self):
        while True:
            respond = self.sock.recv(1024)

    def requestAgent(self):
        #request
        print("yeah~")

    def setUp(self, sock):
        # id
        msg = self.protocolGenerator(1, 0, ["000", "1"])
        self.sock.send(bytes(msg, "utf-8"))
        self.id = self.sock.recv(1024)
        self.id = self.id.decode("utf-8", "ignore").split(",")[2]
        print(self.id)

        # name
        msg = self.protocolGenerator(1, 0, ["001", "1"])
        sock.send(bytes(msg, "utf-8"))
        self.name = sock.recv(1024)
        self.name = self.name.decode("utf-8", "ignore").split(",")[2]
        print(self.name)

        # rank
        msg = self.protocolGenerator(1, 0, ["002", "1"])
        sock.send(bytes(msg, "utf-8"))
        self.rank = sock.recv(1024)
        self.rank = self.rank.decode("utf-8", "ignore").split(",")[2]
        print(self.rank)

        # thumanails
        for i in range(0, 12):
            label = str(100 + i)
            msg = self.protocolGenerator(1, 0, [label, "1"])
            sock.send(bytes(msg, "utf-8"))
            self.tmList[i] = sock.recv(1024).decode("utf-8", "ignore").split(",")[2]
            print(self.tmList[i])
        print("over")


if __name__ == "__main__":
    import GUI.guiHandler as gui
    client = kuflixClient()
    gui.startProgram(client)
