import socket
import threading

class loginServer(object):
    def __init__(self):
        HOST = ''

        PORT = 8080

        self.clientNum = 0;
        self.connectionList = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((HOST, PORT))
        s.listen(1)

        while True:
            self.conn, self.addr = s.accept()

            print('Connected by', self.addr)

            self.connectionList[self.clientNum] = self.conn

            threading._start_new_thread(self.listenClientRequest, (self.connectionList[self.clientNum],))
            self.clientNum += 1

    def protocolGenerator(self, type = 0, flag = None):
        if type == 0: #login protocol ##msgtype | flag
            msg = "00" + flag
            return msg
        else:   #join protocol ##msgtype | flag
            msg = "01" + flag
            return msg

    def listenClientRequest(self, clntSock):
    #    while True:
            request = clntSock.recv(1024)
            request = request.decode("utf-8", "ignore")

            if request[:2] == "00":
                loginInfo = request[2:]
                clntSock.send(bytes(loginInfo, "utf-8"))
            else:
                joinInfo = request[2:]
                clntSock.send(bytes(joinInfo, "utf-8"))

if __name__ == "__main__":
    chattingServer = loginServer()