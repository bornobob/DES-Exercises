import time
from actions.goalaction import GoalAction


class Runner:
    """
    The runner is the class that executes the actions of a Robot.
    """
    def __init__(self, robot, missions):
        """
        Initializer for a Runner.
        :param robot: The Robot that we want to control.
        :param missions: The list of missions that the Robot must perform.
        """
        self.robot = robot
        self.missions = missions

    def couple_robot_to_actions(self, mission):
        """
        Couples a mission to the Robot, coupling the actions to the sensors the Robot has at its disposal.
        """
        for a in mission.actions:
            a.set_robot(self.robot)

    @staticmethod
    def action_may_run(new_action, current_action):
        """
        Detects whether an action may interrupt the running action.
        :param new_action: The action that wants to interrupt.
        :param current_action: The action currently running.
        :return: True if there is no current_action, new_action has a higher priority than current_action or there
        is no currently running action. Returns False otherwise.
        """
        if current_action is None:
            return True
        if new_action.priority > current_action.priority:
            return True
        if not current_action.is_running():
            return True
        return False

    def run(self):
        """
        Sorts the actions in the list of coupled Robot actions by their priority and continuously performs those actions
        in that order.
        """
        for mission in self.missions:
            self.couple_robot_to_actions(mission)
            current_action = None
            sorted_actions = list(sorted(mission.actions, key=lambda x: -x.priority))
            passed_mission = False
            while not passed_mission:
                for a in sorted_actions:
                    if isinstance(a, GoalAction) and a.goal_reached():
                        passed_mission = True
                        self.robot.sensormap.tank_drive.stop()
                        if mission.celebratory_action:
                            mission.celebrate(self.robot)
                        break
                    if a.check():
                        if Runner.action_may_run(a, current_action):
                            if current_action and current_action.is_running():
                                current_action.kill()
                            a.action()
                            current_action = a
                            break
                time.sleep(.1)
