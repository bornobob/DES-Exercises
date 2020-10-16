from actions.baseaction import BaseAction


class ColorDetAction(BaseAction):
    def __init__(self, priority, colors):
        super().__init__(priority)
        self.colors = set(colors)
        self.detected = set()

    def check(self):
        if self.robot.cs.color in self.colors:
            if self.robot.cs.color not in self.detected:
                return True
        return not self.robot.bluetooth.queue.empty()

    def handle_queue(self):
        if not self.robot.bluetooth.queue.empty():
            new_color = self.robot.bluetooth.queue.get()
            self.detected.add(new_color)
            self.robot.speak('You detected a new color')

    def handle_colordetection(self):
        if self.robot.cs.color in self.colors and self.robot.cs.color not in self.detected:
            self.detected.add(self.robot.cs.color)
            self.robot.bluetooth.write(self.robot.cs.color)
            self.robot.speak('I detected a new color')

    def _do_action(self):
        self.handle_queue()
        self.handle_colordetection()
        if self.detected == self.colors:
            self.robot.tank_drive.stop()
            self.robot.leds.animate_cycle(('RED', 'YELLOW', 'BLACK'), duration=10000000)
