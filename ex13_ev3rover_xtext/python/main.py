"""from actions import *
from runner import Runner
from robot import Robot

from utils import *


MAC_ADDRESS = '00:1a:7d:da:71:10'  # Mac address via which the Robots connect with bluetooth
PORT = 4  # Port on which the Robots connect with bluetooth



def create_runner(master=None):
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
"""
from actions import *
from runner import Runner
from robot import Robot


def create_runner():
	r = Robot()
	mission_ToTheMoon = [DriveAction(priority=0), BorderAction(priority=1)]
	mission_ToTheMoon2 = [DriveAction(priority=0), BorderAction(priority=1, rotate_degrees=.5)]
	mission_AllTheColours = [DriveAction(priority=0), BorderAction(priority=10), UltrasoundAction(priority=5), ColorDetAction(priority=3, colors=[5, 4, 2])]
	mission_AllTheColoursButFaster = [DriveAction(priority=0, speed=80), BorderAction(priority=10), UltrasoundAction(priority=5), ColorDetAction(priority=3, colors=[5, 4, 2])]
	Runner(r, mission_ToTheMoon).run()


if __name__ == '__main__':
	create_runner()

