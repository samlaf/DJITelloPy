from djitellopy import Tello
import abc
import threading
import time
import logging
import pygame, pygame.display, pygame.font, pygame.color

class MissionPads(abc.ABC):

    def __init__(self):
        self.thread = threading.Thread(target = self.mission, daemon=True)
        self.thread.start()

    @abc.abstractmethod
    def mission(self):
        pass

class MissionPadsPrinter(MissionPads):

    def __init__(self, tello, cam_direction = 0):
        tello = Tello()
        tello.enable_mission_pads()
        # 0 for below cam, 1 for front cam, 2 for both.
        # front cam doesn't seem to work for me...
        tello.set_mission_pad_detection_direction(cam_direction)
        self.tello = tello

        if pygame.display.get_active():
            self.screen = pygame.display.get_surface()
        else:
            pygame.init()
            self.screen = pygame.display.set_mode([480,320])

        super().__init__()

    def mission(self):
        while True:
            pad = self.tello.get_mission_pad_id()
            x = self.tello.get_mission_pad_distance_x()
            y = self.tello.get_mission_pad_distance_y()
            z = self.tello.get_mission_pad_distance_z()
            text = f"Mission Pad: {pad}\nPos: ({x},{y},{z})"
            myfont = pygame.font.Font(pygame.font.get_default_font(), 100)
            black = pygame.color.THECOLORS['green']
            surf = pygame.font.Font.render(myfont, text, True, black)
            self.screen.blit(surf, (0,0))
            #pygame.display.update()
            time.sleep(1)
    
if __name__ == "__main__":
    tello = Tello()
    tello.connect()

    mpp = MissionPadsPrinter(tello)
    mpp.thread.join()