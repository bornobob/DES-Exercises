from actions.baseaction import BaseAction
from ev3dev2.sensor.lego import ColorSensor


class BorderAction(BaseAction):
    """
    The BorderAction tries to keep the Robot within a black drawn border.
    """
    def check(self):
        return self.robot.cs.color == ColorSensor.COLOR_BLACK

    def _do_action(self):
        self.robot.tank_drive.stop()
        self.robot.rotate_degrees(.3, lock=self.lock)

    def signal(self):
        self.robot.sound.speak("Out of bounds")
