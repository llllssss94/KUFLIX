import socket
import GUI.guiHandler as gui

class kuflixClient(object):
    def __init__(self):
        gui.startProgram(self)

    def protocolGenerator(self, type=0, msgList={}):
        if type == 0:  # login protocol ##msgtype | id | hashed_passward
            msg = "00" + msgList[0] + "," + msgList[1]
            return msg
        else:  # join protocol ##msgtype | id | hashed_passward | name | age
            msg = "01" + msgList[0] + "," + msgList[1] + "," + msgList[2] + "," + msgList[3]
            return msg

    def request(self, msg):
        HOST = "127.0.0.1"
        PORT = 8080

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        s.send(bytes(msg,"utf-8"))

        data = s.recv(1024)

        data = data.decode("utf-8", "ignore")

        print(data.split(",")[0], data.split(",")[1])
        s.close()

if __name__ == "__main__":
    chattingServer = kuflixClient()