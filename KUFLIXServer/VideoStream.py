import cv2, os


class VideoStream:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.capture = cv2.VideoCapture(filename)
            self.wholeFrameNum = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        except:
            raise IOError
        self.frameNum = 0

    def nextFrame(self):
        """Get next frame."""
        data = None
        if self.frameNum < self.wholeFrameNum:
            ret, frame = cv2.VideoCapture.read(self.capture)
            frame = self.image_resize(frame, height=288)

            cv2.imwrite("./tmp/temp.jpg", frame)

            byteSize = os.path.getsize("./tmp/temp.jpg")
            print(byteSize)

            f = open("./tmp/temp.jpg", "rb")

            data = f.read()
            self.frameNum += 1

        return data

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def frameNbr(self):
        """Get frame number."""
        return self.frameNum
