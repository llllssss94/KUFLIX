import socket
import threading
import pickle, os, time, random
import videoPlayer as player

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
                msg = "00" + "," + msgList[0] + "," + self.uid
                return msg
            elif type == 1:  # 01 ##[01 | LABEL | UID]  #thumnail file transfer request
                msg = "01" + "," + msgList[0] + "," + self.uid
                return msg
            elif type == 2:  # 10 ##[10 | MESSAGE | UID]    #request search
                msg = "10" + "," + msgList[0] + "," + self.uid
                return msg
            elif type == 3:  # 11 ##[11 | VIDEO_ID | UID]     #request video streaming
                msg = "11" + "," + msgList[0] + "," + self.uid
                return msg
            else:   # 20 ##[20 | LABEL | UID]   #type = 4, label(200 => recent)
                msg = "20" + "," + msgList[0] + "," + self.uid
                return msg

    def loginRequest(self, msg):
        HOST = "localhost"
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

    def requestList(self):
        print("")

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
            return [msgList[1], msgList[2]]
        elif msgList[0] == "01":  # request thumnail file
            return msgList[1]
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
        elif msgList[0] == "11":  # request streaming # pickle(addr, port)
            streamAddr = msgList[1]
            streamPort = msgList[2]
            rtpPort = str(random.randrange(20000, 40000))
            filename = msgList[3]
            print(streamAddr, streamPort, rtpPort, filename)
            return [streamAddr, streamPort, rtpPort, filename]
        elif msgList[0] == "20":
            dataList = []
            dataList.append(msgList)
            self.sock.send(pickle.dumps("ack"))
            while msgList[3] != "1":
                data = self.sock.recv(1024)
                data = pickle.loads(data)
                msgList = data.split(",")
                dataList.append(msgList)
                self.sock.send(pickle.dumps("ack"))
            return dataList
        else:
            self.sock.close()

    def startPlayer(self, cid = ""):
        info = self.mainRequest(self.protocolGenerator(1, 3, [cid]))

        time.sleep(1)

        vp = player.videoPlayer()
        vp.startPlayer(info[0], info[1], info[2], info[3])

    def listener(self):
        while True:
            respond = self.sock.recv(1024)

    def requestAgent(self, types = 0, label = ""):
        #request
        #protocol 1 - 1 with label, uid
        reponse = self.mainRequest(self.protocolGenerator(1, 1, [label]))
        print(reponse)

        HOST = "127.0.0.1"
        PORT = int(reponse)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((HOST, PORT))
            except ConnectionRefusedError as e:
                continue
            break
        print("connected")
        for i in range(1, 13):
            try :
                os.path.getsize("./thumnails/" + str(int(label) + i) + ".png")
            except FileNotFoundError as e:
                #when server response port_num, then connect to new socket to receieve thumnail file
                self.requestThumnail(label, i, s)
                time.sleep(0.2)
        print("Image recieve success.")
        s.send(pickle.dumps("Done"))
        s.close()

    def requestThumnail(self, label, i, s):
        # when server response port_num, then connect to new socket to receieve thumnail file
        f = open("./thumnails/" + str(int(label) + i) + ".png", "wb")

        s.send(pickle.dumps("rqimg" + str(i)))

        data = s.recv(128)
        print(data)
        frameNum = pickle.loads(data)

        s.send("ack".encode("utf-8"))

        print(frameNum)

        for i in range(0, frameNum):
            data = s.recv(1024)
            f.write(data)
        print("Done")
        f.close()

    def setUp(self, sock):
        # id
        self.id = self.mainRequest(self.protocolGenerator(1, 0, ["000"]))[1]
        print(self.id)

        # name
        self.name = self.mainRequest(self.protocolGenerator(1, 0, ["001"]))[1]
        print(self.name)

        # rank
        self.rank = self.mainRequest(self.protocolGenerator(1, 0, ["002"]))[1]
        if self.rank == "0":
            self.rank = "19+"
        else:
            self.rank = "R"
        print(self.rank)

        #thumnail files
        self.requestAgent(0, "100")

        # thumanails
        for i in range(1, 13):
            label = str(100 + i)
            print(label)
            self.tmList[i] = self.mainRequest(self.protocolGenerator(1, 0, [label]))
            print(self.tmList[i])
        print("over")


if __name__ == "__main__":
    import GUI.guiHandler as gui
    client = kuflixClient()
    gui.startProgram(client)
