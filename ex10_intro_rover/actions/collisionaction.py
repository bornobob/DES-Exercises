from actions.baseaction import BaseAction


class CollisionAction(BaseAction):
    def check(self):
        if self.robot.left_touch.is_pressed:
            self.robot.rotate_degrees(80)
            return True
        elif self.robot.right_touch.is_pressed:
            self.robot.rotate_degrees(-80)
            return True
        return False
