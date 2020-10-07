from actions.baseaction import BaseAction
from ev3dev2.sensor.lego import ColorSensor


class BorderAction(BaseAction):
    def check(self):
        if self.robot.cs.color == ColorSensor.COLOR_BLACK:
            self.robot.rotate_degrees(80)
            return True
        return False
