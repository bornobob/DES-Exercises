class Runner:
    """
    The runner is the class that executes the actions of a Robot.
    """
    def __init__(self, robot, actions):
        """
        Initializer for a Runner.
        :param robot: The Robot that we want to control.
        :param actions: The list of actions that the Robot can perform.
        """
        self.robot = robot
        self.actions = actions
        self.couple_robot_to_actions()

    def couple_robot_to_actions(self):
        """
        Couples the list of actions to the Robot, coupling the actions to the sensors the Robot has at its disposal.
        """
        for a in self.actions:
            a.set_robot(self.robot)

    def run(self):
        """
        Sorts the actions in the list of coupled Robot actions by their priority and continuously performs those actions
        in that order.
        """
        self.robot.start_drive()
        sorted_actions = list(sorted(self.actions, key=lambda x: -x.priority))
        while True:
            for a in sorted_actions:
                if a.check():
                    break
