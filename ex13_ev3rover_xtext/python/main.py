from actions import DriveAction, BorderAction, CollisionAction, UltrasoundAction, MeasureAction, DontDrownAction
from runner import Runner
from ev3dev2.unit import STUD_MM
from robot import Robot
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor, ColorSensor
from ev3dev2.wheel import EV3EducationSetTire
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveDifferential, Motor
from utils import SensorMap, BluetoothMaster


MAC_ADDRESS = '00:1a:7d:da:71:10'  # Mac address via which the Robots connect with bluetooth
PORT = 4  # Port on which the Robots connect with bluetooth

sensor_map_master = {'tank_drive': MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM),
                     'measurement_motor': Motor(OUTPUT_B),
                     'cs_l': ColorSensor('ev3-ports:in1'), 'cs_m': ColorSensor('ev3-ports:in2'),
                     'cs_r': ColorSensor('ev3-ports:in3'), 'us_b': UltrasonicSensor('ev3-ports:in4')}

def create_runner():
	r = Robot(SensorMap(sensor_map_master), bluetooth=BluetoothMaster(MAC_ADDRESS, PORT))
	mission_ToTheMoonAndBeyond = [DriveAction(priority=0), 
						 		  CollisionAction(priority=2),
						 		  UltrasoundAction(priority=8),
					     		  BorderAction(priority=10),
								  DontDrownAction(priority=5, lakes=[ColorSensor.COLOR_RED, ColorSensor.COLOR_BLUE, ColorSensor.COLOR_YELLOW]),
						 		  MeasureAction(priority=6, colors=[ColorSensor.COLOR_RED, ColorSensor.COLOR_BLUE, ColorSensor.COLOR_YELLOW])]
	Runner(r, mission_ToTheMoonAndBeyond).run()


if __name__ == '__main__':
	create_runner()
