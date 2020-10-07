class BaseAction:
    def __init__(self, priority):
        self.robot = None
        self.priority = priority

    def set_robot(self, robot):
        self.robot = robot

    def check(self):
        pass
