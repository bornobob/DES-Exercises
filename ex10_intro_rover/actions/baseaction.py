class BaseAction:
    """
    Base action is only here so other actions can override it.
    Actions are "things" that the robot can follow, so you might have an action that keeps the robot within a certain
    boundary. Or an action that wants to move towards a certain point.
    These actions can be defined in the overriden "check()" function. This function should return False if nothing has
    happened, so in the case of the border, the border was not found. Otherwise True is returned.
    We need this return in the Runner class. In that class we have a list of actions we want to follow, with their
    priorities. Actions are executed in ascending order of priority, if an action returns True, we start again at the
    beginning checking the actions.
    """

    def __init__(self, priority):
        """
        Initialiser for an Action.
        :param priority: The priority of the action.
        """
        self.robot = None
        self.priority = priority

    def set_robot(self, robot):
        """
        Binds a robot to the Action, this is needed since the action needs access to the sensors.
        :param robot:
        :return:
        """
        self.robot = robot

    def check(self):
        """
        The check function should do the check of this Action, returns True if the action was taken, False otherwise.
        """
        pass
