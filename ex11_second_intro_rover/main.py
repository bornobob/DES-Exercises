from actions import BorderAction, UltrasoundAction, CollisionAction
from runner import Runner
from robot import Robot


if __name__ == '__main__':
    r = Robot()
    edge_action = BorderAction(priority=10)
    touch_action = CollisionAction(priority=5)
    see_action = UltrasoundAction(priority=1)
    Runner(r, [edge_action, touch_action, see_action]).run()
