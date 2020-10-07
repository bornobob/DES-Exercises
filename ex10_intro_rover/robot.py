from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor, ColorSensor


class Robot:
    def __init__(self):
        self.cs = ColorSensor()
        self.left_touch = TouchSensor('ev3-ports:in1')
        self.right_touch = TouchSensor('ev3-ports:in4')
        self.us = UltrasonicSensor()
        self.tank_drive = Robot.get_tank_drive()
        self.setup_sensors()

    @staticmethod
    def get_tank_drive():
        return MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)

    def setup_sensors(self):
        self.us.mode = UltrasonicSensor.MODE_US_DIST_CM  # continuous centimeter measurement

    def start_drive(self, speed_percentage=40):
        self.tank_drive.on(SpeedPercent(speed_percentage), SpeedPercent(speed_percentage))

    def reverse_for_rotations(self, nr_rotations, speed_percentage=30):
        self.tank_drive.on_for_rotations(SpeedPercent(-speed_percentage),
                                         SpeedPercent(-speed_percentage),
                                         nr_rotations)

    def rotate_degrees(self, degrees, reverse_before_continue=True, speed_percentage=35):
        self.tank_drive.stop()
        if reverse_before_continue:
            self.reverse_for_rotations(1)
        self.tank_drive.turn_left(SpeedPercent(speed_percentage), degrees)
        self.start_drive()
