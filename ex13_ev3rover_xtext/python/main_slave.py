from runner import Runner
from robot import Robot
from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor
from utils import SensorMap, BluetoothSlave
from actions import DataAction

MAC_ADDRESS = '00:1a:7d:da:71:10'  # Mac address via which the Robots connect with bluetooth
PORT = 4  # Port on which the Robots connect with bluetooth

sensor_map_slave = {'ts_b': TouchSensor('ev3-ports:in1'), 'ts_l': TouchSensor('ev3-ports:in2'),
                    'ts_r': TouchSensor('ev3-ports:in3'), 'us_f': UltrasonicSensor('ev3-ports:in4')}

def create_runner():
	r = Robot(SensorMap(sensor_map_slave), bluetooth=BluetoothSlave(MAC_ADDRESS, PORT))
	Runner(r, [DataAction(1, polling_rate=250)]).run()


if __name__ == '__main__':
	create_runner()
