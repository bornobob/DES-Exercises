import abc

class BaseCelebration(abc.ABC):
    @abc.abstractmethod
    def celebrate(robot):
        """
        Completes some celebration sequence for the robot.
        """
