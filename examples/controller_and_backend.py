from djitellopy import Tello
from djitellopy.controllers import KeyboardVelocityController
from djitellopy.video_backends import VideoStreamBackend
from djitellopy.mission_pads import MissionPadsPrinter

tello = Tello()
tello.connect()
print(tello.get_battery())

# Thing to try
# Create a pygame window and then pass it to video, controller, mp
# so that they all write on the same window!

vsb = VideoStreamBackend()
tello.add_video_callback(vsb)
tello.streamon()

controller = KeyboardVelocityController(tello)

mpp = MissionPadsPrinter(tello)
mpp.thread.join()