from djitellopy import Tello
from djitellopy.controllers import KeyboardVelocityController
from djitellopy.video_backends import VideoStreamBackend
from djitellopy.mission_pads import MissionPadsPrinter
from djitellopy.guis import pygameGUI
import pygame

tello = Tello()
tello.connect()
print(tello.get_battery())

vsb = VideoStreamBackend(tello)
tello.streamon()

controller = KeyboardVelocityController(tello)

mpp = MissionPadsPrinter(tello)

gui = pygameGUI(tello, vsb)
gui.addOSD(mpp)
gui.start()