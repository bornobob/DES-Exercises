from actions.goalaction import GoalAction
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import SpeedRPM


class MeasureAction(GoalAction):
    """
    The MeasureAction is a Goal Action that will try to find all
    the lakes with the given colors and perform measurements on them.
    """
    def __init__(self, priority, colors):
        super().__init__(priority)
        self.colors = set(colors)
        self.detected = set()
        self.detected_with_center = False

    def check(self):
        sensor_values = [self.robot.sensormap.cs_l.color,
                         self.robot.sensormap.cs_r.color,
                         self.robot.sensormap.cs_m.color]
        number_per_color = [sum(1 if v == c and c not in self.detected else 0 for v in sensor_values) for c in self.colors]
        if list(filter(lambda x: x > 1, number_per_color)):
            self.detected_with_center = False
            return True
        elif self.robot.sensormap.cs_m.color in self.colors and \
             self.robot.sensormap.cs_m.color not in self.detected:
            self.detected_with_center = True
            return True
        return False

    def align_from_2_sensors(self):
        # Align the robot to be able to perform a measurement
        while self.robot.sensormap.cs_l.color != self.robot.sensormap.cs_r.color:
            if self.robot.sensormap.cs_l.color == ColorSensor.COLOR_BLACK:
                # the left sensor measures black, meaning we should rotate right a bit
                self.robot.rotate_degrees(.025, reverse_before_continue=False, rpm=5, lock=self.lock)
            else:
                # the right sensor measures black, meaning we should rotate left a bit
                self.robot.rotate_degrees(-.025, reverse_before_continue=False, rpm=5, lock=self.lock)
        while self.robot.sensormap.cs_m.color == ColorSensor.COLOR_BLACK and \
              (self.robot.sensormap.cs_l.color in self.colors or \
               self.robot.sensormap.cs_r.color in self.colors):
            self.robot.reverse_for_rotations(.05, rpm=5, lock=self.lock)

    def align_from_center(self):
        while self.robot.sensormap.cs_l.color != self.robot.sensormap.cs_m.color or \
              self.robot.sensormap.cs_r.color != self.robot.sensormap.cs_m.color:
            self.robot.reverse_for_rotations(-.05, rpm=5, lock=self.lock)
    
    def get_lake_color(self):
        if self.robot.sensormap.cs_l.color in self.colors:
            return self.robot.sensormap.cs_l.color
        elif self.robot.sensormap.cs_r.color in self.colors:
            return self.robot.sensormap.cs_r.color
        elif self.robot.sensormap.cs_m.color in self.colors:
            return self.robot.sensormap.cs_m.color
        return None

    def _do_action(self):
        self.robot.sensormap.tank_drive.stop()
        if self.detected_with_center:
            self.align_from_center()
        else:
            self.align_from_2_sensors()
        # Now we know we are aligned
        self.robot.sensormap.measurement_motor.on_for_rotations(SpeedRPM(-5), .3)
        if self.get_lake_color():
            self.detected.add(self.get_lake_color())
        self.robot.sensormap.measurement_motor.on_for_rotations(SpeedRPM(5), .3)
        self.robot.rotate_degrees(.25, lock=self.lock)
        self.goal_passed = self.colors == self.detected
