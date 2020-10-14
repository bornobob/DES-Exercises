from actions import *
from runner import Runner
from robot import Robot


if __name__ == '__main__':
    r = Robot()
    edge_action = BorderAction(priority=10)
    touch_action = CollisionAction(priority=5)
    see_action = UltrasoundAction(priority=1)
    drive_action = DriveAction(priority=0)
    Runner(r, [edge_action, touch_action, see_action, drive_action]).run()
