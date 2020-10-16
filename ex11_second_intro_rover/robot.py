from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM, SpeedPercent, SpeedDPS
from ev3dev2.unit import STUD_MM
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from datetime import datetime, timedelta
import time


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

    def reverse_for_rotations(self, nr_rotations, rpm=60, lock=None):
        """
        Reverses the Robot (makes it move backwards).
        :param nr_rotations: Number of degrees Robot turns.
        :param rpm: Speed at which the Robot reverses in rotations per minute.
        :param lock: Optional Lock to stop the operation when requested
        """
        self.tank_drive.on_for_rotations(SpeedRPM(-rpm), SpeedRPM(-rpm), nr_rotations, block=False)
        end_time = datetime.now() + timedelta(seconds=(nr_rotations*60)/rpm)
        while datetime.now() < end_time:
            if lock.is_locked():
                self.tank_drive.stop()
                break
            time.sleep(0.01)

    def turn_for_rotations(self, rotations, rpm=30, lock=None):
        """
        Turn for a number of degrees with the given speed.
        Can be pre-empted when given a Lock.
        :param rotations: The number of rotations to turn.
        :param rpm: The speed to turn at.
        :param lock: Optional Lock to stop the operation when requested.
        """
        self.tank_drive.on_for_rotations(SpeedRPM(rpm), SpeedRPM(-rpm), abs(rotations), block=False)
        end_time = datetime.now() + timedelta(seconds=(abs(rotations)*60)/abs(rpm))
        while datetime.now() < end_time:
            if lock.is_locked():
                self.tank_drive.stop()
                break
            time.sleep(0.01)

    def rotate_degrees(self, rotations, reverse_before_continue=True, rpm=35, lock=None):
        """
        Rotates the Robot.
        :param rotations: Number of rotations the Robot rotates.
        :param reverse_before_continue: True if Robot needs to reverse before turning, False if not.
        :param rpm: Speed at which the Robot turns.
        :param lock: Optional Lock to stop the operation when requested
        """
        if reverse_before_continue:
            self.reverse_for_rotations(.6, lock=lock)
        self.turn_for_rotations(rotations, rpm=rpm, lock=lock)
