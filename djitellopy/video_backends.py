import cv2
from djitellopy import Tello
import time

class VideoStreamBackend:

    count = 1

    def __init__(self, size=None, name=None):
        self.size = size
        if name is None:
            self.name = "VideoStream{}".format(VideoStreamBackend.count)
            VideoStreamBackend.count += 1
    
    def __call__(self, img):
        if self.size is not None:
            img = cv2.resize(img, self.size)
        cv2.imshow(self.name, img)
        cv2.waitKey(1)

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    print(tello.get_battery())
    vsb1 = VideoStreamBackend()
    vsb2 = VideoStreamBackend(size=(320,240))
    tello.add_video_callback(vsb1)
    tello.add_video_callback(vsb2)
    tello.streamon()
    time.sleep(30)
    tello.end()