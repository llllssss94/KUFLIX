import sys, signal
from tkinter import Tk
from Client import Client


def signal_handler(signal, frame):
    print('Goodbye!')
    sys.exit(0)


if __name__ == "__main__":
    # setup terminator
    signal.signal(signal.SIGINT,signal_handler)
    try:
        serverAddr = "127.0.0.1"
        serverPort = "5005" ##for rtsp
        rtpPort = str(int(serverPort) + 30000)
        fileName = "SampleVideo_1280x720_30mb.mp4"
    except:
        print("[Usage: ClientLauncher.py Server_name Server_port RTP_port Video_file]")

    root = Tk()

    # Create a new client
    app = Client(root, serverAddr, serverPort, rtpPort, fileName)
    app.master.title("RTPClient")
    root.mainloop()
