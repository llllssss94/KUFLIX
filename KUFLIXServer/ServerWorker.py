from random import randint
import sys, traceback, threading, socket
import pickle, wave

from VideoStream import VideoStream
from RtpPacket import RtpPacket

class ServerWorker:
    SETUP = 'SETUP'
    PLAY = 'PLAY'
    PAUSE = 'PAUSE'
    TEARDOWN = 'TEARDOWN'

    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT

    OK_200 = 0
    FILE_NOT_FOUND_404 = 1
    CON_ERR_500 = 2

    clientInfo = {}

    def __init__(self, clientInfo, mainSocket = None, agentSeqNum = None):
        self.clientInfo = clientInfo
        self.waveFile = None
        self.mainSock = mainSocket
        self.agentSeqNum = agentSeqNum

    def run(self):
        threading.Thread(target=self.recvRtspRequest).start()

    def recvRtspRequest(self):
        """Receive RTSP request from the client."""
        connSocket = self.clientInfo['rtspSocket'][0]
        while True:
            data = connSocket.recv(256)
            if data:
                data = pickle.loads(data)
                print("Data received:", data)
                self.processRtspRequest(data)

    def processRtspRequest(self, data):
        """Process RTSP request sent from the client."""
        # Get the request type
        request = data.split('\n')
        line1 = request[0].split(' ')
        requestType = line1[0]

        # Get the media file DBid
        filename = line1[1]

        # Get the RTSP sequence number
        seq = request[1].split(' ')

        # Process SETUP request
        if requestType == self.SETUP:
            if self.state == self.INIT:
                # Update state
                print("processing SETUP")

                try:
                    absName = filename[:filename.__len__() - (filename.split(".")[filename.split(".").__len__() - 1].__len__() + 1)]
                    self.clientInfo['videoStream'] = VideoStream("./contents/" + filename)# it must be a path
                    self.waveFile = wave.open('./contents/' + absName + '.wav', 'rb')
                    self.state = self.READY
                except IOError:
                    self.replyRtsp(self.FILE_NOT_FOUND_404, seq[1])

                # Generate a randomized RTSP session ID
                self.clientInfo['session'] = randint(100000, 999999)

                # Send RTSP reply
                self.replyRtsp(self.OK_200, seq[1])

                # Get the RTP/UDP port from the last line
                self.clientInfo['rtpPort'] = request[2].split(' ')[3]

        # Process PLAY request
        elif requestType == self.PLAY:
            if self.state == self.READY:
                print("processing PLAY")
                self.state = self.PLAYING

                # Create a new socket for RTP/UDP
                self.clientInfo["rtpSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.clientInfo["waveSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                self.replyRtsp(self.OK_200, seq[1])

                # Create a new thread and start sending RTP packets
                self.clientInfo['event'] = threading.Event()
                self.clientInfo['worker']= threading.Thread(target=self.sendRtp)
                self.clientInfo['wave'] = threading.Thread(target=self.sendWave)
                self.clientInfo['wave'].start()
                self.clientInfo['worker'].start()

        # Process PAUSE request
        elif requestType == self.PAUSE:
            if self.state == self.PLAYING:
                print("processing PAUSE")
                self.state = self.READY

                self.clientInfo['event'].set()

                self.replyRtsp(self.OK_200, seq[1])

        # Process TEARDOWN request
        elif requestType == self.TEARDOWN:
            print("processing TEARDOWN")

            self.clientInfo['event'].set()

            self.replyRtsp(self.OK_200, seq[1])

            # Close the RTP socket
            self.clientInfo['rtpSocket'].close()

            self.mainSock.send(pickle.dumps("out," + str(self.agentSeqNum)))

    def sendWave(self):
        """Send RTP packets over UDP."""
        fps = self.clientInfo['videoStream'].getFps()
        runningTime = self.clientInfo['videoStream'].getWholeFrameNum() / fps
        wholeAudioFrame = self.waveFile.getnframes()
        afps = wholeAudioFrame / runningTime

        CHUNK = int(afps / (fps + 4))   ## audio frame num of one video frame (FOR MAXIMIZE AUDIO QUALITY)
        print("chunk",CHUNK)

        while True:
            self.clientInfo['event'].wait(0.05)

            # Stop sending if request is PAUSE or TEARDOWN
            if self.clientInfo['event'].isSet():
                break

            data = self.waveFile.readframes(CHUNK)      ##get audio frame from wave file
            if data:
                try:
                    address = self.clientInfo['rtspSocket'][1][0]
                    port = int(self.clientInfo['rtpPort']) + 20000

                    self.clientInfo["waveSocket"].sendto(data, (address, port))
                    print("sendWave")
                except:
                    print("Connection Error")
                    print('-'*60)
                    traceback.print_exc(file=sys.stdout)
                    print('-'*60)


    def sendRtp(self):
        """Send RTP packets over UDP."""
        while True:
            self.clientInfo['event'].wait(0.05)

            # Stop sending if request is PAUSE or TEARDOWN
            if self.clientInfo['event'].isSet():
                break

            data = self.clientInfo['videoStream'].nextFrame()   #full byte of frame
            if data:
                frameNumber = self.clientInfo['videoStream'].frameNbr()
                try:
                    address = self.clientInfo['rtspSocket'][1][0]
                    port = int(self.clientInfo['rtpPort'])
                    packet = self.makeRtp(data, frameNumber)
                    while packet.__len__() != 0:
                        self.clientInfo['rtpSocket'].sendto(packet[:20480],(address,port))
                        packet = packet[20480:]
                    self.clientInfo['rtpSocket'].sendto("EOF".encode('utf-8'), (address, port))
                    print("sendEOF")
                except:
                    print("Connection Error")
                    print('-'*60)
                    traceback.print_exc(file=sys.stdout)
                    print('-'*60)

    def makeRtp(self, payload, frameNbr):
        """RTP-packetize the video data."""
        version = 2
        padding = 0
        extension = 0
        cc = 0
        marker = 0
        pt = 26 # MJPEG type
        seqnum = frameNbr
        ssrc = 0

        rtpPacket = RtpPacket()

        rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)

        return rtpPacket.getPacket()

    def replyRtsp(self, code, seq):
        """Send RTSP reply to the client."""
        if code == self.OK_200:
            #print "200 OK"
            reply = 'RTSP/1.0 200 OK\nCSeq: ' + seq + '\nSession: ' + str(self.clientInfo['session'])
            connSocket = self.clientInfo['rtspSocket'][0]
            reply = pickle.dumps(reply)
            connSocket.send(reply)

        # Error messages
        elif code == self.FILE_NOT_FOUND_404:
            print("404 NOT FOUND")
        elif code == self.CON_ERR_500:
            print("500 CONNECTION ERROR")
