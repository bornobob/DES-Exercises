from actions.baseaction import BaseAction


class DriveAction(BaseAction):
    """
    The DriveAction always tries to drive the Robot forward.
    """
    def __init__(self, priority, speed=40):
        super().__init__(priority)
        self.speed = speed

    def check(self):
        return True

    def _do_action(self):
        self.robot.start_drive(self.speed)
