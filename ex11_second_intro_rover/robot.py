from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveDifferential
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound


class Robot:
    """
    Robot is a class that instantiates and sets up the robot so that it is ready for use. It initializes the sensors
    and the tank drive, and it sets up the sensors. On top of that it provides functions so that the robot can be
    controlled.
    """
    def __init__(self):
        """
        Initializer for a Robot.
        """
        self.cs = ColorSensor()
        self.left_touch = TouchSensor('ev3-ports:in1')
        self.right_touch = TouchSensor('ev3-ports:in4')
        self.us = UltrasonicSensor()
        self.tank_drive = Robot.get_tank_drive()
        self.sound = Sound()
        self.leds = Leds()
        self.setup_sensors()

    @staticmethod
    def get_tank_drive():
        """
        Loads the setup of the motors of a Robot. Contains the motor outputs, the type of tire and
        the distance between the two wheels of the robot.
        :return: A tank_drive setup with the two motors, tire type and distance between tires.
        """
        return MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM)

    def setup_sensors(self):
        """
        Sets up the "modes" of the sensors. For example sets the ultrasonic sensor to continuous centimeter measurement.
        """
        self.us.mode = UltrasonicSensor.MODE_US_DIST_CM  # continuous centimeter measurement

    def start_drive(self, speed_percentage=40):
        """
        Activates the motors of the robot to move forward.
        :param speed_percentage: The speed of the Robot based on motor power. Percentage between 0 and 100.
        """
        self.tank_drive.on(SpeedPercent(speed_percentage), SpeedPercent(speed_percentage))

    def reverse_for_rotations(self, nr_rotations, speed_percentage=30):
        """
        Reverses the Robot (makes it move backwards).
        :param nr_rotations: Number of degrees Robot turns.
        :param speed_percentage: Speed at which the Robot reverses. Percentage between 0 and 100.
        """
        step_size = .05
        for _ in range(0, int(nr_rotations * (1 / step_size))):
            self.tank_drive.on_for_rotations(SpeedPercent(-speed_percentage),
                                             SpeedPercent(-speed_percentage),
                                             step_size)

    def rotate_degrees(self, degrees, reverse_before_continue=True, speed_percentage=35):
        """
        Rotates the Robot.
        :param degrees: Number of degrees the Robot is moved from its current position.
        :param reverse_before_continue: True if Robot needs to reverse before turning, False if not.
        :param speed_percentage: Speed at which the Robot turns. Percentage between 0 and 100.
        """
        self.tank_drive.stop()
        if reverse_before_continue:
            self.reverse_for_rotations(1)
        self.tank_drive.turn_left(SpeedPercent(speed_percentage), degrees)
        self.start_drive()
