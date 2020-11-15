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
