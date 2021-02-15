""" 
Here we implement different controllers that send commands to the Tello:
   - CLI controller
   - keyboard controller
   - joystick controller
"""
import abc
import threading
import time
import pygame, pygame.display
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
        if pygame.display.get_active():
            self.screen = pygame.display.get_surface()
        else:
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

class KeyboardVelocityController(Controller):

    def __init__(self, tello, FPS=120, speed=50):
        self.tello = tello
        self.FPS = FPS
        self.speed = speed
        tello.set_speed(speed)
        self.is_flying = False
        
        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0

        if pygame.display.get_active():
            self.screen = pygame.display.get_surface()
        else:
            pygame.init()
            self.screen = pygame.display.set_mode([480,320])

        super().__init__()

    def command_parser(self):

        should_stop = False
        while not should_stop:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)
            
            if self.is_flying:
                self.tello.send_rc_control(self.left_right_velocity, 
                                            self.for_back_velocity,
                                            self.up_down_velocity, 
                                            self.yaw_velocity)
            time.sleep(1 / self.FPS)

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = self.speed
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -self.speed
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -self.speed
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = self.speed
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = self.speed
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -self.speed
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -self.speed
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = self.speed
    
    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.is_flying = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.is_flying = False
        elif key == pygame.K_1:
            self.speed = 10
        elif key == pygame.K_2:
            self.speed = 20
        elif key == pygame.K_3:
            self.speed = 30
        elif key == pygame.K_4:
            self.speed = 40
        elif key == pygame.K_5:
            self.speed = 50
        elif key == pygame.K_6:
            self.speed = 60
        elif key == pygame.K_7:
            self.speed = 70
        elif key == pygame.K_8:
            self.speed = 80
        elif key == pygame.K_9:
            self.speed = 90
        elif key == pygame.K_0:
            self.speed = 100

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    print(tello.get_battery())
    controller = KeyboardVelocityController(tello)
    controller.thread.join()