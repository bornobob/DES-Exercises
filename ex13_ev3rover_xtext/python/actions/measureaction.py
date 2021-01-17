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
                         self.robot.sensormap.cs_r.color]
        return any(s in self.colors and not s in self.detected for s in sensor_values)

    def align(self):
        # Align the robot to be able to perform a measurement
        bounces = 0  # keep track of alignment bounces
        # when we reach more than three bounces, we agree that the robot is sufficiently aligned
        # iff two out of three sensors show a non black color
        # otherwise, the left and right sensors have to show the same non black color
        while not (self.robot.sensormap.cs_l.color == self.robot.sensormap.cs_r.color and self.robot.sensormap.cs_l.color != ColorSensor.COLOR_BLACK) and \
              not (bounces > 3 and self.robot.sensormap.cs_l.color == self.robot.sensormap.cs_m.color and self.robot.sensormap.cs_l.color != ColorSensor.COLOR_BLACK) and \
              not (bounces > 3 and self.robot.sensormap.cs_r.color == self.robot.sensormap.cs_m.color and self.robot.sensormap.cs_r.color != ColorSensor.COLOR_BLACK): 
            if self.robot.sensormap.cs_l.color == ColorSensor.COLOR_BLACK:
                # the left sensor measures black, meaning we should rotate right a bit
                # we rotate right until the right color sensor is no longer black
                while self.robot.sensormap.cs_r.color != ColorSensor.COLOR_BLACK:
                    self.robot.rotate_degrees(.005, reverse_before_continue=False, rpm=5, lock=self.lock)
            else:
                # the right sensor measures black, meaning we should rotate left a bit
                # we rotate left until the left color sensor is no longer black
                while self.robot.sensormap.cs_l.color != ColorSensor.COLOR_BLACK:
                    self.robot.rotate_degrees(-.005, reverse_before_continue=False, rpm=5, lock=self.lock)
            while self.robot.sensormap.cs_l.color == ColorSensor.COLOR_BLACK and self.robot.sensormap.cs_r.color == ColorSensor.COLOR_BLACK:
                # now we drive forward until either of the left or right color sensor is a non black color
                self.robot.reverse_for_rotations(-0.02, rpm=5, lock=self.lock)
            bounces += 1
        while self.robot.sensormap.cs_m.color == ColorSensor.COLOR_BLACK:
            # finally, if the middle sensor is black, we reverse until it is not
            self.robot.reverse_for_rotations(.05, rpm=5, lock=self.lock)

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
        self.align()
        # Now we know we are aligned
        self.robot.sensormap.measurement_motor.on_for_rotations(SpeedRPM(-5), .3)
        if self.get_lake_color():
            self.detected.add(self.get_lake_color())
        self.robot.sensormap.measurement_motor.on_for_rotations(SpeedRPM(5), .3)
        self.robot.rotate_degrees(.25, lock=self.lock)
        self.goal_passed = self.colors == self.detected
