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

    def reverse_for_rotations(self, nr_rotations, speed_percentage=30, lock=None):
        """
        Reverses the Robot (makes it move backwards).
        :param nr_rotations: Number of degrees Robot turns.
        :param speed_percentage: Speed at which the Robot reverses. Percentage between 0 and 100.
        :param lock: Optional Lock to stop the operation when requested
        """
        step_size = .2
        for _ in range(0, int(nr_rotations * (1 / step_size))):
            if not lock or not lock.is_locked():
                self.tank_drive.on_for_rotations(SpeedPercent(-speed_percentage),
                                                 SpeedPercent(-speed_percentage),
                                                 step_size)
            else:
                return

    def turn_for_rotations(self, degrees, speed_percentage=30, lock=None):
        """
        Turn for a number of degrees with the given speed.
        Can be pre-empted when given a Lock.
        :param degrees: The number of degrees to turn.
        :param speed_percentage: The speed to turn at.
        :param lock: Optional Lock to stop the operation when requested.
        """
        for i in range(0, abs(degrees//4)):
            print('rotating: ', i, '/', degrees // 4 , lock.is_locked())
            if not lock or not lock.is_locked():
                print('lock checked, was not locked')
                self.tank_drive.turn_left(SpeedPercent(speed_percentage), 4 if degrees > 0 else -4)
                print('moved')
            else:
                print('lock checked, was locked, exiting')
                return

    def rotate_degrees(self, degrees, reverse_before_continue=True, speed_percentage=35, lock=None):
        """
        Rotates the Robot.
        :param degrees: Number of degrees the Robot is moved from its current position.
        :param reverse_before_continue: True if Robot needs to reverse before turning, False if not.
        :param speed_percentage: Speed at which the Robot turns. Percentage between 0 and 100.
        :param lock: Optional Lock to stop the operation when requested
        """
        if reverse_before_continue:
            self.reverse_for_rotations(0.4, lock=lock)
        print('done reversing')
        self.turn_for_rotations(degrees, speed_percentage=speed_percentage, lock=lock)
        print('done rotating')
