from actions.baseaction import BaseAction
from ev3dev2.sensor.lego import ColorSensor


class BorderAction(BaseAction):
    """
    The BorderAction tries to keep the Robot within a black drawn border.
    """
    def __init__(self, priority, rotate_degrees=.3):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees
        self.turn_right = False

    def check(self):
        if self.robot.sensormap.cs_l.color == ColorSensor.COLOR_WHITE:
            self.turn_right = True
        elif self.robot.sensormap.cs_r.color == ColorSensor.COLOR_WHITE:
            self.turn_right = False
        elif self.robot.sensormap.cs_m.color == ColorSensor.COLOR_WHITE:
            self.turn_right = True
        else:
            return False
        return True

    def _do_action(self):
        self.robot.sensormap.tank_drive.stop()
        if self.turn_right:
            self.robot.rotate_degrees(self.rotate_degrees, lock=self.lock)
        else:
            self.robot.rotate_degrees(-self.rotate_degrees, lock=self.lock)
