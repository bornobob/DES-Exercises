from actions.baseaction import BaseAction


class GoalAction(BaseAction):
    """
    The DriveAction always tries to drive the Robot forward.
    """
    def __init__(self, priority):
        super().__init__(priority)
        self.goal_passed = False

    def goal_reached(self):
        return self.goal_passed
