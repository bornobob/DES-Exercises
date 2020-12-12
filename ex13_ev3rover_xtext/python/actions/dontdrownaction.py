from actions.baseaction import BaseAction
from ev3dev2.sensor.lego import ColorSensor


class DontDrownAction(BaseAction):
    """
    The DontDrownAction tries to keep the Robot out of the lakes.
    """
    def __init__(self, priority, lakes, rotate_degrees=.3):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees
        self.lakes = lakes
        self.turn_right = False

    def check(self):
        if self.robot.sensormap.cs_l.color in self.lakes:
            self.turn_right = True
        elif self.robot.sensormap.cs_r.color in self.lakes:
            self.turn_right = False
        elif self.robot.sensormap.cs_m.color in self.lakes:
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
