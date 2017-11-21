import socket
import threading
import cx_Oracle
import pickle
import shutil, datetime

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

        s.bind((HOST, PORT))
        s.listen(1)

        self.DBcommunicator(self.sqlGenerator(1))

        while True:
            self.conn, self.addr = s.accept()

            print('Connected by', self.addr)

            data = self.conn.recv(1024)
            uid = data.decode("utf-8", "ignore")
            print("uid = ", uid)

            self.conn.send(bytes("ack", "utf-8"))

            self.connectionList[self.clientNum] = [self.conn, uid]
            threading._start_new_thread(self.listenClientRequest, (self.connectionList[self.clientNum][0],))
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
        else:           #11 ##[11 | PORT_NUM]   send signal of streaming with a new port number
            msg = "11" + "," + msgList[0]
            return msg

    def listenClientRequest(self, clntSock):
        while True:
            request = clntSock.recv(1024)
            request = pickle.loads(request)
            print("request :" , request)

            if request[:2] == "00": #request string info of first page
                msg = request[2:]
                print(msg)
                self.respond(clntSock, msg)
            elif request[:2] == "01":   #request thumnail file
                msg = request[2:]
                self.agentHandler(1, msg)
            elif request[:2] == "10":   #request search
                msg = request[2:]
                self.search(clntSock, msg)
            elif request[:2] == "11":   #request streaming
                msg = request[2:]
                self.agentHandler(2, msg)
            else:
                clntSock.close()

    def respond(self, clntSock, request = ""):    #send first page string data to client
        label = request.split(",")[1]
        print(label)
        uid = request.split(",")[2]
        print(uid)
        if label[0] == "0": #db request require uid
            #select id, name ,rank info from database with uid
            print("info request")
            msg = self.protocolGenerator(0, ["000", "yourID"])
            clntSock.send(pickle.dumps(msg))
        else:   #without uid
            #select fetured thumnail's name
            print("thum request")
            msg = self.protocolGenerator(0, ["101", "thumnailName1"])
            clntSock.send(pickle.dumps(msg))

    def search(self, clntSock, keyword = None):
        #select search result with keyword
        keyword = keyword.split(",")[1]
        dbResponse = self.DBcommunicator(self.sqlGenerator(2, [keyword,]))
        print(dbResponse)

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
            sql = "SELECT count(*) from videos"
            return sql
        elif type == 5:
            print("delete")

    def DBcommunicator(self, sql = ""):
        self.cursor.execute(sql)
        try:
            result = self.cursor.fetchall()
            return result
        except cx_Oracle.InterfaceError as e:
            self.cursor.execute("COMMIT")
            print("update")

    def agentHandler(self, type = 0, request = ""):
        print("mka")

    def makeFileTransferAgent(self, portNum = 0, TID = ""):
        print("mftp")

    def makeStreamingAgent(self, portNum = 0, CID =""):
        print("mst")

    def uploadNewContents(self, path = ""):
        currentTime = datetime.datetime.now()
        currentTime = currentTime.strftime('%Y-%m-%d')
        conNum = self.DBcommunicator(self.sqlGenerator(4))
        print(conNum)
        conNum = str(int(conNum[0][0]) + 1)

        path = path.split("/")[path.split("/").__len__() - 1]

        print(self.sqlGenerator(3, [conNum, path, "0", "0", currentTime]))
        self.DBcommunicator(self.sqlGenerator(3, [conNum, path, "0", "0", currentTime]))

        shutil.copy(path, "contents")


if __name__ == "__main__":
    import GUI.guiHandler as gui
    chattingServer = kufilxServer()
    gui.startProgram(chattingServer)
    chattingServer.mainLoop()