import socket
import threading
import pickle

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
            if type == 0:  # 00 ##[00 | LABEL | UID]    #first page info
                msg = "00" + "," + msgList[0] + "," + msgList[1]
                return msg
            elif type == 1:  # 01 ##[01 | LABEL | UID]  #thumnail file transfer request
                msg = "01" + "," + msgList[0] + "," + msgList[1]
                return msg
            elif type == 2:  # 10 ##[10 | MESSAGE | UID]    #request search
                msg = "10" + "," + msgList[0] + "," + msgList[1]
                return msg
            else:  # 11 ##[11 | VIDEO_ID | UID]     #request video streaming
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
                s.close()
                return "nop"
            else:
                s.close()
                self.uid = msgList[2]   #save uid
                print("uid : ", self.uid , "port : ", port)
                self.mainLoop(port)
                return "success"
        else:
            flag = msgList[1]
            if flag == "0":
                s.close()
                return "nop"
            else:
                s.close()
                return "success"

        #Through return value, system signal to GUIhandler what has to be

    def mainLoop(self, port):
        HOST = "127.0.0.1"
        PORT = 8100  # port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        print("Mainserver connected")

        self.sock.send(bytes(self.uid, "utf-8"))
        print("send")

        ack = self.sock.recv(1024)

        self.setUp(self.sock)

    def mainRequest(self, msg):
        self.sock.send(pickle.dumps(msg))

        data = self.sock.recv(1024)

        data = pickle.loads(data)

        msgList = data.split(",")

        if msgList[0] == "00":  # request string info of first page
            return msgList[2]
        elif msgList[0] == "01":  # request thumnail file
            return [msgList[1], msgList[2]]
        elif msgList[0] == "10":  # request search
            searchList = []
            searchList.append(msgList)
            self.sock.send(pickle.dumps("ack"))
            while msgList[3] != "1":
                data = self.sock.recv(1024)
                data = pickle.loads(data)
                msgList = data.split(",")
                searchList.append(msgList)
                self.sock.send(pickle.dumps("ack"))
            return searchList
        elif msgList[0] == "11":  # request streaming
            print("streaming")
        else:
            self.sock.close()

    def listener(self):
        while True:
            respond = self.sock.recv(1024)

    def requestAgent(self):
        #request
        print("yeah~")

    def setUp(self, sock):
        # id
        self.id = self.mainRequest(self.protocolGenerator(1, 0, ["000", "1"]))
        print(self.id)

        # name
        self.name = self.mainRequest(self.protocolGenerator(1, 0, ["001", "1"]))
        print(self.name)

        # rank
        self.rank = self.mainRequest(self.protocolGenerator(1, 0, ["002", "1"]))
        print(self.rank)

        # thumanails
        for i in range(0, 12):
            label = str(100 + i)
            self.tmList[i] = self.mainRequest(self.protocolGenerator(1, 0, [label, "1"]))
            print(self.tmList[i])
        print("over")


if __name__ == "__main__":
    import GUI.guiHandler as gui
    client = kuflixClient()
    gui.startProgram(client)
