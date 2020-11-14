from actions import *
from runner import Runner
from robot import Robot
from ev3dev2.sensor.lego import ColorSensor
from utils import *


MAC_ADDRESS = '00:1a:7d:da:71:10'  # Mac address via which the Robots connect with bluetooth
PORT = 4  # Port on which the Robots connect with bluetooth
COLORS = [ColorSensor.COLOR_RED, ColorSensor.COLOR_YELLOW, ColorSensor.COLOR_BLUE]  # List of colors to be detected


def create_runner(master=None):
    """
    Creates a running thread of a Robot, either a bluetooth master or slave and initializes all the actions it can take.
    :param master: True if the Robot is a bluetooth master device, False if it is a bluetooth slave device. None if
    no bluetooth is required.
    """
    if master:
        r = Robot(BluetoothMaster(MAC_ADDRESS, PORT))
    elif master is not None:
        r = Robot(BluetoothSlave(MAC_ADDRESS, PORT))
    else:
        r = Robot()
    edge_action = BorderAction(priority=10)
    touch_action = CollisionAction(priority=5)
    see_action = UltrasoundAction(priority=1)
    drive_action = DriveAction(priority=0)
    color_action = ColorDetAction(priority=8, colors=[COLORS])
    Runner(r, [edge_action, touch_action, see_action, drive_action, color_action]).run()


if __name__ == '__main__':
    create_runner()
