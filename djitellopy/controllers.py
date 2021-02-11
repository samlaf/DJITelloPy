""" 
Here we implement different controllers that send commands to the Tello:
   - CLI controller
   - keyboard controller
   - joystick controller
"""
import abc
import threading
import time
import pygame
from djitellopy import Tello

class Controller(abc.ABC):
    def __init__(self):
        self.thread = threading.Thread(target = self.command_parser, daemon=True)
        self.thread.start()

    @abc.abstractmethod
    def command_parser(self):
        pass

class CLIController(Controller):

    def __init__(self, tello):
        self.CMD_TO_METHOD = {
            "takeoff": tello.takeoff,
            "land": tello.land,
            "forward": tello.move_forward,
            "back": tello.move_back,
            "left": tello.move_left,
            "right": tello.move_right,
            "up": tello.move_up,
            "down": tello.move_down,
            "cw": tello.rotate_clockwise,
            "ccw": tello.rotate_counter_clockwise
        }
        super().__init__()


    def command_parser(self):
        print("")
        print("Command line controller: enter one of the following commands to control the Tello:")
        print("takeoff land forward back left right up down cw ccw")
        print("Press <enter> without a command to exit command line controller")
        print()
        while True:
            try:
                msg = input("")
                if not msg:
                    break
                cmd_and_arg = msg.split()
                cmd = cmd_and_arg[0]
                tellomethod = self.CMD_TO_METHOD[cmd]
                if len(cmd_and_arg) == 1:
                    tellomethod()
                elif len(cmd_and_arg) == 2:
                    arg = int(cmd_and_arg[1])
                    tellomethod(arg)
            except KeyboardInterrupt:
                print("Exiting...")
                break
            except Exception:
                print("Not a valid command.")

class KeyboardCommandController(Controller):
    
    def __init__(self, tello, FPS=120):
        self.tello = tello
        self.FPS = FPS
        pygame.init()
        self.screen = pygame.display.set_mode([480,320])
        super().__init__()

    def command_parser(self):
        on = True
        while on:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.tello.takeoff()
                    elif event.key == pygame.K_l:
                        self.tello.land()
                    elif event.key == pygame.K_ESCAPE:
                        on = False
                        break
                    elif event.key == pygame.K_UP:
                        self.tello.move_forward(30)
                    elif event.key == pygame.K_DOWN:
                        self.tello.move_back(30)
                    elif event.key == pygame.K_LEFT:
                        self.tello.move_left(30)
                    elif event.key == pygame.K_RIGHT:
                        self.tello.move_right(30)
                    elif event.key == pygame.K_d:
                        self.tello.rotate_clockwise(30)
                    elif event.key == pygame.K_a:
                        self.tello.rotate_counter_clockwise(30)
                    elif event.key == pygame.K_w:
                        self.tello.move_up(30)
                    elif event.key == pygame.K_s:
                        self.tello.move_down(30)
            time.sleep(1/self.FPS)
        pygame.display.quit()

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    controller = CLIController(tello)
    controller.thread.join()
    tello.end()
