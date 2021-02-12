import cv2
from djitellopy import Tello

class VideoStreamBackend:

    count = 1

    def __init__(self, size=None, name=None):
        self.size = size
        if name is None:
            self.name = "VideoStream{}".format(VideoStreamBackend.count)
            VideoStreamBackend.count += 1
    
    def callback(self, img):
        if self.size is not None:
            img = cv2.resize(img, self.size)
        cv2.imshow(self.name, img)

if __name__ == "__main__":
    tello = Tello()
    vsb1 = VideoStreamBackend()
    vsb2 = VideoStreamBackend()
    #tello.add_video_callback(vsb1.callback)
    tello.connect()
    #tello.streamon()