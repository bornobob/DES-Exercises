from actions.baseaction import BaseAction


class CollisionAction(BaseAction):
    """
    The Collision Action turns around a bit when bumping into an object by checking the Touch Sensors
    """
    def check(self):
        return self.robot.right_touch.is_pressed or self.robot.left_touch.is_pressed

    def _do_action(self):
        if self.robot.left_touch.is_pressed:
            self.robot.rotate_degrees(degrees=80, lock=self.lock)
        elif self.robot.right_touch.is_pressed:
            self.robot.rotate_degrees(degrees=-80, lock=self.lock)

    def signal(self):
        pass
