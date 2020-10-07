from actions.baseaction import BaseAction


class UltrasoundAction(BaseAction):
    def check(self):
        if -1 < self.robot.us.value() <= 300:
            self.robot.rotate_degrees(35, reverse_before_continue=False)
            return True
        return False
