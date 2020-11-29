from actions.baseaction import BaseAction
from ev3dev2.sensor.lego import ColorSensor


class BorderAction(BaseAction):
    """
    The BorderAction tries to keep the Robot within a black drawn border.
    """
    def __init__(self, priority, rotate_degrees=.3):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees

    def check(self):
        return self.robot.sensormap.cs_l.color == ColorSensor.COLOR_WHITE

    def _do_action(self):
        self.robot.sensormap.tank_drive.stop()
        self.robot.rotate_degrees(self.rotate_degrees, lock=self.lock)
