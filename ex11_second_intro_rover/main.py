from actions import *
from runner import Runner
from robot import Robot
from ev3dev2.sensor.lego import ColorSensor
from utils import *


MAC_ADDRESS = '00:1a:7d:da:71:10'
PORT = 4


def create_runner(master):
    if master:
        r = Robot(BluetoothMaster(MAC_ADDRESS, PORT))
    else:
        r = Robot(BluetoothSlave(MAC_ADDRESS, PORT))
    edge_action = BorderAction(priority=10)
    touch_action = CollisionAction(priority=5)
    see_action = UltrasoundAction(priority=1)
    drive_action = DriveAction(priority=0)
    color_action = ColorDetAction(priority=8, colors=[ColorSensor.COLOR_RED, ColorSensor.COLOR_YELLOW,
                                                      ColorSensor.COLOR_BLUE])
    Runner(r, [edge_action, touch_action, see_action, drive_action, color_action]).run()


if __name__ == '__main__':
    create_runner(False)
