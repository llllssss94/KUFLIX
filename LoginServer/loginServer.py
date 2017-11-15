import socket
import threading
import cx_Oracle

class loginServer(object):
    def __init__(self):
        HOST = ''

        PORT = 8080

        self.clientNum = 0;
        self.connectionList = {}
        self.dbConn = cx_Oracle.connect("scott/tiger@117.16.136.70:1521/orcl")
        self.cursor = self.dbConn.cursor()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((HOST, PORT))
        s.listen(1)

        while True:
            self.conn, self.addr = s.accept()

            print('Connected by', self.addr)

            self.connectionList[self.clientNum] = self.conn

            threading._start_new_thread(self.listenClientRequest, (self.connectionList[self.clientNum],))
            self.clientNum += 1

    def protocolGenerator(self, type = 0, flag = None, uid = "0000"): #flag: 0000(failed), main_Server_PortNum(success)
        if type == 0: #login protocol ##msgtype | flag | uid(default 0000)
            msg = "00" + "," + flag + "," + uid
            return msg
        else:   #join protocol ##msgtype | flag (0 , 1) 0 is fail
            msg = "01" + "," + flag
            return msg

    def listenClientRequest(self, clntSock):
        request = clntSock.recv(1024)
        request = request.decode("utf-8", "ignore")
        msgList = request.split(",")

        if request[:2] == "00":     ##respond uid
            #db check~~ and get uid
            msg = self.protocolGenerator(0, "8100", "1")
            clntSock.send(bytes(msg, "utf-8"))
        else:   ##respond join result
            id = msgList[1]
            passwd = msgList[2]
            name = msgList[3]
            age = msgList[4]
            # db insert new user
            msg = self.protocolGenerator(1, "1")
            clntSock.send(bytes(msg, "utf-8"))
        clntSock.close()

    def sqlGenerator(self, type = 0):
        if type == 0:   #chaeck login
            sql = "SELECT memberid, age, rank FROM members"
            self.DBcommunicator(sql)
        elif type == 1: #regester new user
            sql = "SELECT contentsname FROM videos WHERE cid IN (SELECT cid FROM feturedcontent)"
            self.DBcommunicator(sql)

    def DBcommunicator(self, sql = ""):
        self.cursor.execute(sql)

if __name__ == "__main__":
    chattingServer = loginServer()