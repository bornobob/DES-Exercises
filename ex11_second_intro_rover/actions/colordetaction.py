from actions.baseaction import BaseAction


class ColorDetAction(BaseAction):
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
        if self.robot.cs.color in self.colors:
            if self.robot.cs.color not in self.detected:
                return True
        if self.robot.bluetooth:
            return not self.robot.bluetooth.queue.empty()
        return False

    def handle_queue(self):
        """
        If the Robot has a bluetooth connection, then it checks if there is a message in the queue. If there is a
        message in the queue, the color is added to the set "detected" and a signal is given.
        """
        if not self.robot.bluetooth.queue.empty():
            new_color = self.robot.bluetooth.queue.get()
            self.detected.add(new_color)
            self.robot.speak('You detected a new color')

    def handle_colordetection(self):
        """
        If Robot detects a color and the color is a new color, it is added to the set "detected". If the Robot has a
        bluetooth connection, it also sends out a message containing that color via its connection. Finally signals
        that it has found a color.
        """
        if self.robot.cs.color in self.colors and self.robot.cs.color not in self.detected:
            self.detected.add(self.robot.cs.color)
            if self.robot.bluetooth:
                self.robot.bluetooth.write(self.robot.cs.color)
            self.robot.speak('I detected a new color')

    def _do_action(self):
        if self.robot.bluetooth:
            self.handle_queue()
        self.handle_colordetection()
        if self.detected == self.colors:
            self.robot.tank_drive.stop()
            self.robot.leds.animate_cycle(('RED', 'YELLOW', 'BLACK'), duration=10000000)
