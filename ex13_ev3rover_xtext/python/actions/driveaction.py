from actions.baseaction import BaseAction


class DriveAction(BaseAction):
    """
    The DriveAction always tries to drive the Robot forward.
    """
    def check(self):
        return True

    def _do_action(self):
        self.robot.start_drive(40)
