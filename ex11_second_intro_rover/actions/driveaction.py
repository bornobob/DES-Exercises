from actions.baseaction import BaseAction


class DriveAction(BaseAction):
    def check(self):
        return True

    def _do_action(self):
        self.robot.start_drive(40)
