from utils import Lock
from threading import Thread


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
        self.lock = Lock()
        self.action_thread = None

    def set_robot(self, robot):
        """
        Binds a robot to the Action, this is needed since the action needs access to the sensors.
        """
        self.robot = robot

    def check(self):
        """
        The check function should do the check of this Action, returns True if the action needs to be taken, False
        otherwise.
        """
        pass

    def _do_action(self):
        """
        This function should implement the actual action taken when check() returns True.
        Note that this function should be using the Lock, when the Lock is locked, this function should be stopped ASAP.
        """
        pass

    def _action_then_signal(self):
        self._do_action()
        if not self.lock.is_locked():
            self.signal()

    def is_running(self):
        return self.action_thread and self.action_thread.is_alive()

    def action(self):
        self.action_thread = Thread(target=self._action_then_signal, daemon=True)
        self.action_thread.start()

    def kill(self):
        self.lock.lock()
        if self.action_thread:
            self.action_thread.join()
        self.lock.unlock()

    def signal(self):
        """
        The signal function should give a signal of this Action.
        """
        pass
