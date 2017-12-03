import socket
import threading
import cx_Oracle
import hashlib

class loginServer(object):
    def __init__(self):
        HOST = ''

        PORT = 8080

        self.clientNum = 0;
        self.connectionList = {}
        self.dbConn = cx_Oracle.connect("scott/tiger@117.16.136.70:1521/orcl")
        self.cursor = self.dbConn.cursor()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempt to open Server")
        while True:
            try:
                s.bind((HOST, PORT))
            except OSError as e:
                continue
            break
        print("Server Open Success")
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
            inputID = msgList[1]
            inputPW = msgList[2]
            dbResponse = self.DBcommunicator(self.sqlGenerator(0, [inputID, ]))

            sessionKey = self.DBcommunicator(self.sqlGenerator(5, [str(dbResponse[0][1])]))[0][0]
            if sessionKey != 0:
                msg = self.protocolGenerator(0, "0000", "0000")
                clntSock.send(bytes(msg, "utf-8"))
                print("login failed")
            else:
                if dbResponse[0][0] == inputPW:
                    print("login success")
                    msg = self.protocolGenerator(0, "8100", str(dbResponse[0][1]))
                    clntSock.send(bytes(msg, "utf-8"))
                    self.DBcommunicator(self.sqlGenerator(4, [str(dbResponse[0][1])]))
                else:
                    msg = self.protocolGenerator(0, "0000", "0000")
                    clntSock.send(bytes(msg, "utf-8"))
                    print("login failed")
        else:   ##respond join result
            id = msgList[1]
            passwd = hashlib.sha256(bytes(msgList[2], "utf-8")).hexdigest()
            name = msgList[3]
            age = msgList[4]
            if int(age) > 18 :
                rank = "0"
            else:
                rank = "1"

            try:
                if int(self.DBcommunicator(self.sqlGenerator(1, [id,]))[0][0]) == 0:
                    userNum = self.DBcommunicator(self.sqlGenerator(2))
                    userNum = str(int(userNum[0][0]) + 1)
                    self.DBcommunicator(self.sqlGenerator(3, [userNum, id, passwd, name, age, rank]))
                    msg = self.protocolGenerator(1, "1", )
                    clntSock.send(bytes(msg, "utf-8"))
                else:
                    print("ID already exists.")
                    msg = self.protocolGenerator(1, "0", )
                    clntSock.send(bytes(msg, "utf-8"))
            except cx_Oracle.DatabaseError as e:
                print(e)

            msg = self.protocolGenerator(1, "1")
            clntSock.send(bytes(msg, "utf-8"))
        clntSock.close()

    def sqlGenerator(self, type = 0, msgList = []):
        if type == 0:   #chaeck login
            sql = "SELECT hashPW, mid FROM members WHERE memberid = '" + msgList[0] + "'"
            return sql
        elif type == 1:
            sql = "SELECT count(*) FROM members WHERE memberid = '" + msgList[0] + "'"
            return sql
        elif type == 2:
            sql = "SELECT count(*) FROM members"
            return sql
        elif type == 3: #regester new user
            sql = "INSERT INTO members(mid, memberid, hashPW, membername, age, rank) VALUES ('" + msgList[0] + "', '" + msgList[1] + "', '" + msgList[2] + "', '" + msgList[3] + "', '" + msgList[4] + "', '" + msgList[5] + "')"
            return sql
        elif type == 4:
            sql = "INSERT INTO sessionList(mid) values ('" + msgList[0] + "')"
            return sql
        elif type == 5:
            sql = "SELECT count(*) FROM sessionList WHERE mid = '" + msgList[0] + "'"
            return sql

    def DBcommunicator(self, sql = ""):
        self.cursor.execute(sql)
        try:
            result = self.cursor.fetchall()
            return result
        except cx_Oracle.InterfaceError as e:
            self.cursor.execute("COMMIT")
            print("update")

if __name__ == "__main__":
    chattingServer = loginServer()