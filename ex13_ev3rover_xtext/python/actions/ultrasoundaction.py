from actions.baseaction import BaseAction


class UltrasoundAction(BaseAction):
    """
    The Ultrasound Action tries to prevent bumping into objects by checking the Ultrasound Sensor.
    """
    def __init__(self, priority, rotate_degrees=.3):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees

    def check(self):
        return -1 < self.robot.us.value() <= 300

    def _do_action(self):
        self.robot.rotate_degrees(rotations=self.rotate_degrees, reverse_before_continue=False, lock=self.lock)
