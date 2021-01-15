from actions.goalaction import GoalAction


class PushRockAction(GoalAction):
    """
    The PushRockAction Action tries to push the rocks on Mars either into a lake or off of the planet.
    """
    def __init__(self, priority, number_of_rocks):
        super().__init__(priority)
        self.number_of_rocks = number_of_rocks
        self.pushed_off = 0
        self.pushing = False

    def check(self):
        if not self.robot.database.ts_l is None and not self.robot.database.ts_r is None:
            return (self.robot.database.ts_l or self.robot.database.ts_r) != self.pushing
        return False

    def _do_action(self):
        print('in push rock action')
        self.pushing = not self.pushing
        if not self.pushing:
            self.pushed_off += 1
            if self.pushed_off == self.number_of_rocks:
                self.goal_passed = True
