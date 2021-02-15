from djitellopy import Tello
from djitellopy.controllers import KeyboardVelocityController
from djitellopy.video_backends import VideoStreamBackend
from djitellopy.mission_pads import MissionPadsPrinter
import threading
import pygame

tello = Tello()
tello.connect()
print(tello.get_battery())

cv = threading.Condition()
vsb = VideoStreamBackend(cv)
tello.add_video_callback(vsb)
tello.streamon()

controller = KeyboardVelocityController(tello)

#mpp = MissionPadsPrinter(tello)

while True:
    with cv:
        cv.wait()
        pygame.display.update()