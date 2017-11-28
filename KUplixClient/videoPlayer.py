from tkinter import Tk
import cv2, sys, signal
import Client as player

class videoPlayer(object):

    def __init__(self):
        # setup terminator
        signal.signal(signal.SIGINT, self.signal_handler)
        self.serverAddr = ""
        self.serverPort = ""
        self.rtpPort = ""
        self.filename = ""

    def startPlayer(self, addr, rtspPort, rtpPort, filename):
        self.serverAddr = addr
        self.serverPort = rtspPort
        self.rtpPort = rtpPort
        self.filename = filename

        root = Tk()

        # Create a new client
        app = player.Client(root, self.serverAddr, self.serverPort, self.rtpPort, self.filename)
        app.master.title("RTPClient")
        root.mainloop()

    def signal_handler(signal, frame):
        print('Goodbye!')
        sys.exit(0)
