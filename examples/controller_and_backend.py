from djitellopy import Tello
from djitellopy.controllers import KeyboardCommandController
from djitellopy.video_backends import VideoStreamBackend

tello = Tello()
tello.connect()
print(tello.get_battery())

vsb = VideoStreamBackend()
tello.add_video_callback(vsb)
tello.streamon()

controller = KeyboardCommandController(tello)
controller.thread.join()