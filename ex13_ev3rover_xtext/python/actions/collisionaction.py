from actions.baseaction import BaseAction


class CollisionAction(BaseAction):
    """
    The Collision Action turns around a bit when bumping into an object by checking the Touch Sensors.
    """
    def __init__(self, priority, rotate_degrees=.4, rpm=30):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees
        self.rpm = rpm

    def check(self):
        return self.robot.right_touch.is_pressed or self.robot.left_touch.is_pressed

    def _do_action(self):
        if self.robot.left_touch.is_pressed:
            self.robot.rotate_degrees(rotations=self.rotate_degrees, lock=self.lock, rpm=self.rpm)
        elif self.robot.right_touch.is_pressed:
            self.robot.rotate_degrees(rotations=self.rotate_degrees, lock=self.lock, rpm=-self.rpm)
