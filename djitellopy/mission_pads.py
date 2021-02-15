from djitellopy import Tello
import threading
import time
import pygame, pygame.display, pygame.font, pygame.color

class MissionPadsPrinter():

    def __init__(self, tello, cam_direction = 0):
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
        self.surf1 = self.screen
        self.surf2 = self.screen
        tello.add_state_callback(self)

    def __call__(self, datadict):
        pad = datadict['mid']
        x = datadict['x']
        y = datadict['y']
        z = datadict['z']
        myfont = pygame.font.Font(pygame.font.get_default_font(), 20)
        red = pygame.color.THECOLORS['red']
        line1 = f"Mission Pad: {pad}"
        self.surf1 = pygame.font.Font.render(myfont, line1, True, red)
        line2 = f"Pos: ({x},{y},{z})"
        self.surf2 = pygame.font.Font.render(myfont, line2, True, red)
    
    def draw(self):
        self.screen.blit(self.surf1, (0,0))
        self.screen.blit(self.surf2, (0,self.surf1.get_height()))


if __name__ == "__main__":
    tello = Tello()
    tello.connect()

    mpp = MissionPadsPrinter(tello)

    while True:
        cv = tello.get_cv()
        with cv:
            cv.wait()
            mpp.draw()
            pygame.display.update()