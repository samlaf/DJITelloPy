import cv2
from djitellopy import Tello
import time
import pygame, pygame.display
import threading
import numpy as np

class VideoStreamBackend:

    count = 1

    def __init__(self, cv, size=None, name=None):
        self.cv = cv
        if size is None:
            self.size = (480, 320)
        else:
            self.size = size
        
        if name is None:
            self.name = "VideoStream{}".format(VideoStreamBackend.count)
            VideoStreamBackend.count += 1
        else:
            self.name = name
        
        if pygame.display.get_active():
            self.screen = pygame.display.get_surface()
        else:
            pygame.init()
            self.screen = pygame.display.set_mode([480,320])
    
    def __call__(self, img):
        # cv2 imgs use BGR and use hxw (instead of wxh)
        img = cv2.resize(img, self.size)
        img = np.transpose(img, (1,0,2))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        surf = pygame.surfarray.make_surface(img)
        with self.cv:
            self.screen.blit(surf, (0,0))
            self.cv.notify()

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    print(tello.get_battery())
    cv = threading.Condition()
    vsb1 = VideoStreamBackend(cv)
    tello.add_video_callback(vsb1)
    # vsb2 = VideoStreamBackend(cv, size=(320,240))
    # tello.add_video_callback(vsb2)
    tello.streamon()
    while True:
        with cv:
            cv.wait()
            pygame.display.update()