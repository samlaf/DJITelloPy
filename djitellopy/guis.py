import pygame

class pygameGUI:

    def __init__(self, tello, video_backend):
        self.tello = tello
        self.video_backend = video_backend
        self.OSDs = []

    def addOSD(self, osd):
        self.OSDs.append(osd)

    def start(self):
        while True:
            cv = self.tello.get_cv()
            with cv:
                cv.wait()
                self.video_backend.draw()
                for osd in self.OSDs:
                    osd.draw()
                pygame.display.update()

