class Runner:
    def __init__(self, robot, actions):
        self.robot = robot
        self.actions = actions
        self.couple_robot_to_actions()

    def couple_robot_to_actions(self):
        for a in self.actions:
            a.set_robot(self.robot)

    def run(self):
        self.robot.start_drive()
        sorted_actions = list(sorted(self.actions, key=lambda x: -x.priority))
        while True:
            for a in sorted_actions:
                if a.check():
                    break
