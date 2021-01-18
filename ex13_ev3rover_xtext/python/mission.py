class Mission:
    def __init__(self, actions, celebratory_action=None):
        self.actions = actions
        self.celebratory_action = celebratory_action

    def celebrate(self, robot):
        self.celebratory_action.celebrate(robot)
