from actions.baseaction import BaseAction


class UltrasoundAction(BaseAction):
    """
    The Ultrasound Action tries to prevent bumping into objects by checking the Ultrasound Sensor.
    """
    def __init__(self, priority, rotate_degrees=.3, dodge_rocks=True):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees
        self.dodge_rocks = dodge_rocks

    def check(self):
        return (self.dodge_rocks and \
                self.robot.database.us_f and \
                -1 < self.robot.database.us_f <= 300) or \
               (self.robot.sensormap.us_b.value() > 20)

    def _do_action(self):
        self.robot.rotate_degrees(rotations=self.rotate_degrees, reverse_before_continue=False, lock=self.lock)
