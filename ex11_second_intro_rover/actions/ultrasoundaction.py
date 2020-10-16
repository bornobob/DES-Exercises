from actions.baseaction import BaseAction


class UltrasoundAction(BaseAction):
    """
    The Ultrasound Action tries to prevent bumping into objects by checking the Ultrasound Sensor
    """
    def check(self):
        return -1 < self.robot.us.value() <= 300

    def _do_action(self):
        self.robot.rotate_degrees(rotations=.3, reverse_before_continue=False, lock=self.lock)

    def signal(self):
        pass
