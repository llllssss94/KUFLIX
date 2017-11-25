import socket
import threading
import cx_Oracle
import pickle
import os, shutil, datetime

class kufilxServer(object):
    def __init__(self):
        self.dbConn = cx_Oracle.connect("scott/tiger@117.16.136.70:1521/orcl")
        self.cursor = self.dbConn.cursor()
        self.clientNum = 0
        self.connectionList = {}
        self.agentList = {}

    def mainLoop(self):
        HOST = ''

        PORT = 8100
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen(1)

        print("we are listneing.")

        while True:
            self.conn, self.addr = s.accept()

            print('Connected by', self.addr)

            data = self.conn.recv(1024)
            uid = data.decode("utf-8", "ignore")
            print("uid = ", uid)

            self.conn.send(bytes("ack", "utf-8"))

            self.connectionList[self.clientNum] = [self.conn, uid]
            threading._start_new_thread(self.listenClientRequest, (self.connectionList[self.clientNum][0], uid))
            self.clientNum += 1

    def protocolGenerator(self, type = 0, msgList = []):
        if type == 0:   #00 ##[00 | LABEL | MESSAGE]  send first page string info
            msg = "00" + "," + msgList[0] + "," + msgList[1]
            return msg
        elif type == 1: #01 ##[01 | PORT_NUM]   send signal of filetransfer for thumnail image with a new port number
            msg = "01" + "," + msgList[0]
            return msg
        elif type == 2: #10 ##[10 | MESSAGE | FLAG]   send search result one column by column with continue, end flag signal
            msg = "10" + "," + msgList[0] + "," + msgList[1]
            return msg
        elif type ==3:           #11 ##[11 | PORT_NUM]   send signal of streaming with a new port number
            msg = "11" + "," + msgList[0]
            return msg
        else:       #20 ##[20 | MESSAGE | FLAG] send subList one column by column with contunue end flag signal
            msg = "20" + "," + msgList[0] + "," + msgList[1]
            return msg

    def listenClientRequest(self, clntSock, mid):
        while True:
            try:
                request = clntSock.recv(1024)
            except OSError as e:
                print("yeah!")
                clntSock.close()
                print()
                self.DBcommunicator(self.sqlGenerator(9, [mid]))
                break

            try:
                request = pickle.loads(request)
                print("request :" , request)
            except EOFError as e:
                clntSock.close()
                continue

            if request[:2] == "00": #request string info of first page
                msg = request[2:]
                print(msg)
                self.respond(clntSock, msg)
            elif request[:2] == "01":   #request thumnail file
                msg = request[3:].split(",")   #label(3), uid
                self.agentHandler(1, msg, clntSock)
            elif request[:2] == "10":   #request search
                msg = request[2:]
                self.search(clntSock, msg)
            elif request[:2] == "11":   #request streaming
                msg = request[3:].split(",")   #cid, uid
                self.agentHandler(2, msg, clntSock)
            elif request[:2] == "20":
                msg = request[3:]
                self.getListData(clntSock, msg)
            else:
                clntSock.close()

    def getListData(self, clntSock, msg):
        msg = msg.split(",")
        uid = msg[1]
        if msg[0] == "200":
            dbResponse = self.DBcommunicator(self.sqlGenerator(10, uid))
            print(dbResponse)
            if dbResponse.__len__() != 0:
                for i in range(0, dbResponse.__len__()):
                    msg = str(dbResponse[i][1]) + "," + str(dbResponse[i][2])
                    print(i, "and", dbResponse.__len__())
                    if i + 1 == dbResponse.__len__():
                        msg = self.protocolGenerator(2, [msg, "1"])
                    else:
                        msg = self.protocolGenerator(2, [msg, "0"])
                    print(msg)
                    clntSock.send(pickle.dumps(msg))
                    clntSock.recv(1024)
            else:
                msg = self.protocolGenerator(2, ["No History Found, No History Founded", "1"])
                clntSock.send(pickle.dumps(msg))
                clntSock.recv(1024)
        else:
            dbResponse = self.DBcommunicator(self.sqlGenerator(11, uid))
            print(dbResponse)
            if dbResponse.__len__() != 0:
                for i in range(0, dbResponse.__len__()):
                    msg = str(dbResponse[i][1]) + "," + str(dbResponse[i][2])
                    print(i, "and", dbResponse.__len__())
                    if i + 1 == dbResponse.__len__():
                        msg = self.protocolGenerator(2, [msg, "1"])
                    else:
                        msg = self.protocolGenerator(2, [msg, "0"])
                    print(msg)
                    clntSock.send(pickle.dumps(msg))
                    clntSock.recv(1024)
            else:
                msg = self.protocolGenerator(2, ["No Subscribe Found, No Subscribe Founded", "1"])
                clntSock.send(pickle.dumps(msg))
                clntSock.recv(1024)

    def respond(self, clntSock, request = ""):    #send first page string data to client
        label = request.split(",")[1]
        uid = request.split(",")[2]
        print(uid)
        if label[0] == "0": #db request require uid
            if label[2] == "0":
                values = "memberid"
            elif label[2] == "1":
                values = "membername"
            else:
                values = "rank"
            #select id, name ,rank info from database with uid
            db_response = self.DBcommunicator(self.sqlGenerator(7, [values, uid]))
            print("info request")
            print(db_response[0][0])
            msg = self.protocolGenerator(0, [label, str(db_response[0][0])])
            clntSock.send(pickle.dumps(msg))
        else:   #without uid
            #select fetured thumnail's name
            # TODO and get contentname from videos
            db_response = self.DBcommunicator(self.sqlGenerator(8, [str(int(label) - 100)]))
            print("thum request")
            msg = self.protocolGenerator(0, [db_response[0][0], str(db_response[0][1])])
            clntSock.send(pickle.dumps(msg))

    def search(self, clntSock, keyword = None):
        #select search result with keyword
        keyword = keyword.split(",")[1]
        dbResponse = self.DBcommunicator(self.sqlGenerator(2, [keyword,]))
        print(dbResponse)
        if dbResponse.__len__() != 0:
            for i in range(0, dbResponse.__len__()):
                msg = str(dbResponse[i][0]) + "," + dbResponse[i][1]
                print(i, "and", dbResponse.__len__())
                if i + 1 == dbResponse.__len__():
                    msg = self.protocolGenerator(2, [msg, "1"])
                else :
                    msg = self.protocolGenerator(2, [msg, "0"])
                print(msg)
                clntSock.send(pickle.dumps(msg))
                clntSock.recv(1024)
        else:
            msg = self.protocolGenerator(2, ["No Contents Found, No Contents Founded", "1"])
            clntSock.send(pickle.dumps(msg))
            clntSock.recv(1024)

    def sqlGenerator(self, type = 0, msgList = []):
        if type == 0:   #get profile info
            sql = "SELECT memberid, age, rank FROM members"
            return sql
        elif type == 1: #get thumnail info
            sql = "SELECT contentsname FROM videos WHERE cid IN (SELECT cid FROM feturedcontent)"
            return sql
        elif type == 2: #search result
            sql = "SELECT cid, contentsname FROM videos WHERE contentsname LIKE '%" + msgList[0] + "%'"
            return sql
        elif type == 3: #register new contents to video database
            sql = "INSERT INTO videos(cid, contentsname, contentslength, rank, uploaddate) VALUES ('" + msgList[0] + "', '" + msgList[1] + "', '" + msgList[2] + "', '" + msgList[3] + "', TO_DATE('" + msgList[4] + "', 'YYYY-MM-DD'))"
            return sql
        elif type == 4: #select videos num
            sql = "SELECT MAX(cid) FROM videos"
            return sql
        elif type == 5:
            sql = "DELETE FROM videos WHERE cid = '" + msgList[0] + "'"
            return sql
        elif type == 6:
            sql = "SELECT contentsname FROM videos WHERE cid = '" + msgList[0] + "'"
            return sql
        elif type == 7:
            sql = "SELECT " + msgList[0] + " FROM members WHERE mid = '" + msgList[1] + "'"
            return sql
        elif type == 8:
            sql = "SELECT contentsname, cid FROM videos WHERE cid = (SELECT cid FROM feturedcontent WHERE tid = '" + msgList[0] + "')"
            return sql
        elif type == 9:
            sql = "DELETE FROM sessionList WHERE mid = '" + msgList[0] + "'"
            return sql
        elif type == 10:
            sql = "SELECT * FROM (SELECT videos.cid, videos.contentsname, history.watchdate, history.mid FROM videos, history where videos.cid = history.cid) WHERE mid = '" + msgList[0] + "'"
            return sql
        elif type == 11:
            sql = "SELECT * FROM (SELECT videos.cid, videos.contentsname, sublist.mid FROM videos, sublist where videos.cid = sublist.cid) WHERE mid = '" + msgList[0] + "'"
            return sql

    def DBcommunicator(self, sql = ""):
        self.cursor.execute(sql)
        try:
            result = self.cursor.fetchall()
            return result
        except cx_Oracle.InterfaceError as e:
            self.cursor.execute("COMMIT")
            print("update")

    def agentHandler(self, type = 0, request = [], clntSock = None):
        if type == 1:
            newPort = 10000 + int(request[1])
            msg = self.protocolGenerator(1, [str(newPort)])
            clntSock.send(pickle.dumps(msg))
            self.makeFileTransferAgent(newPort)
        #type 1 => thumnail agent, caculate new portnum with uid (10000 + int(uid)) and tid with label and response portnum
        #type 2 => streaming agent, caculate new portnum with uid (12000 + int(uid)) and cid with cid and response portnum

    def makeFileTransferAgent(self, portNum = 0):
        #get path from database using tid [feturedcontent(tid, cid, path)]
        #open new socket accept
        HOST = ''
        PORT = portNum

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((HOST, PORT))
        s.listen(1)

        conn, addr = s.accept()

        print("connected by ", addr)

        for i in range(1, 13):
            try :
                rqst = conn.recv(1024)
                rqst = pickle.loads(rqst)
            except EOFError as e:
                continue

            if rqst != "rqimg":
                continue

            #send thumnail file
            f = open("./thumnails/" + str(i) + ".png", "rb")  # actually path from database
            size = os.path.getsize("./thumnails/" + str(i) + ".png")
            frameNum = int(size / 1024) + 1

            conn.send(pickle.dumps(frameNum))
            ack = conn.recv(36)

            for i in range(0, frameNum):
                data = f.read(1024)
                conn.send(data)

            print("Done")

            f.close()
        print("image send success")

    def uploadNewContents(self, path = ""):
        currentTime = datetime.datetime.now()
        currentTime = currentTime.strftime('%Y-%m-%d')
        conNum = self.DBcommunicator(self.sqlGenerator(4))
        try :
            conNum = str(int(conNum[0][0]) + 1)
        except TypeError as e:
            conNum = "1"

        path = path.split("/")[path.split("/").__len__() - 1]

        print(self.sqlGenerator(3, [conNum, path, "0", "0", currentTime]))
        self.DBcommunicator(self.sqlGenerator(3, [conNum, path, "0", "0", currentTime]))

        shutil.copy(path, "contents")

    def deleteContents(self, cid):
        os.remove("./contents/" + self.DBcommunicator(self.sqlGenerator(6, [cid]))[0][0])
        self.DBcommunicator(self.sqlGenerator(5, [cid]))

    def getContentsList(self):
        dbResponse = self.DBcommunicator(self.sqlGenerator(2, [""]))
        return dbResponse

    def makeStreamingAgent(self, portNum = 0, CID =""):
        print("mst")

if __name__ == "__main__":
    import GUI.guiHandler as gui
    chattingServer = kufilxServer()
    gui.startProgram(chattingServer)