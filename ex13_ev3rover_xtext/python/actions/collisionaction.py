from actions.baseaction import BaseAction


class CollisionAction(BaseAction):
    """
    The Collision Action turns around a bit when bumping into an object by checking the Touch Sensors.
    """
    def __init__(self, priority, rotate_degrees=.4):
        super().__init__(priority)
        self.rotate_degrees = rotate_degrees
        self.back_touch_is_pressed = False
        self.rotate_right = False

    def check(self):
        if self.robot.database.ts_b:
            self.back_touch_is_pressed = True
        elif self.robot.database.ts_r:
            self.rotate_right = False
        elif self.robot.database.ts_l:
            self.rotate_right = True
        else:
            return False
        return True

    def _do_action(self):
        print(self.robot.database.data)
        if self.back_touch_is_pressed:
            self.robot.rotate_degrees(rotations=self.rotate_degrees, reverse_before_continue=False, lock=self.lock)
        elif self.rotate_right:
            self.robot.rotate_degrees(rotations=self.rotate_degrees, lock=self.lock)
        else:
            self.robot.rotate_degrees(rotations=-self.rotate_degrees, lock=self.lock)
