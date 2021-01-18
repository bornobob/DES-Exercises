from actions.goalaction import GoalAction


class ColorDetAction(GoalAction):
    """
    The ColorDetAction detects the colors on the ground. Stops and displays the found colors once it has found all the
    specified colors.
    """
    def __init__(self, priority, colors):
        """
        Initializer for the ColorDetAction action.
        :param colors: List of colors the Robot has to find.
        """
        super().__init__(priority)
        self.colors = set(colors)
        self.detected = set()

    def check(self):
        sensor_values = [self.robot.sensormap.cs_l.color,
                         self.robot.sensormap.cs_r.color,
                         self.robot.sensormap.cs_m.color]
        return any(s in self.colors and not s in self.detected for s in sensor_values)

    def handle_colordetection(self):
        """
        If Robot detects a color and the color is a new color, it is added to the set "detected". 
        """
        self.robot.sensormap.tank_drive.stop()
        if self.robot.sensormap.cs_l.color in self.colors and self.robot.sensormap.cs_l.color not in self.detected:
            self.detected.add(self.robot.sensormap.cs_l.color)
        elif self.robot.sensormap.cs_r.color in self.colors and self.robot.sensormap.cs_r.color not in self.detected:
            self.detected.add(self.robot.sensormap.cs_r.color)
        elif self.robot.sensormap.cs_m.color in self.colors and self.robot.sensormap.cs_m.color not in self.detected:
            self.detected.add(self.robot.sensormap.cs_m.color)

    def _do_action(self):
        self.handle_colordetection()
        if self.detected == self.colors:
            self.goal_passed = True
