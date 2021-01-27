package lego.rover.generator

import java.util.List
import lego.rover.mission.*

class PyGenerator {
	def static SlaveToText()'''
	from runner import Runner
	from robot import Robot
	from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor
	from utils import SensorMap, BluetoothSlave
	from actions import DataAction
	from mission import Mission
	«"\n\n"»
	MAC_ADDRESS = '00:1a:7d:da:71:10'  # Mac address via which the Robots connect with bluetooth
	PORT = 4  # Port on which the Robots connect with bluetooth
	«"\n"»
	sensor_map_slave = {'ts_b': TouchSensor('ev3-ports:in1'), 'ts_l': TouchSensor('ev3-ports:in2'),
	                    'ts_r': TouchSensor('ev3-ports:in3'), 'us_f': UltrasonicSensor('ev3-ports:in4')}
	«"\n"»
	def create_runner():
		r = Robot(SensorMap(sensor_map_slave), bluetooth=BluetoothSlave(MAC_ADDRESS, PORT))
		Runner(r, [Mission([DataAction(1, polling_rate=250)])]).run()
	«"\n\n"»
	if __name__ == '__main__':
		create_runner()
	'''
	
	def static MainToText()'''
	import subprocess
	import time
	«"\n\n"»
	PYTHON_EXECUTABLE = 'python'
	BRICK_1_PY = 'main_main.py'
	BRICK_2_PY = 'main_slave.py'
	«"\n\n"»
	if __name__ == "__main__":
	    proc1 = subprocess.Popen([PYTHON_EXECUTABLE, BRICK_1_PY])
	    time.sleep(1)
	    proc2 = subprocess.Popen([PYTHON_EXECUTABLE, BRICK_2_PY])
	«"\n"»
	    input('Press [enter] to stop the simulation')
	    proc2.kill()
	    proc1.kill()
	'''
	
	def static ToText(Missions simulation)'''
		from actions.measureaction import MeasureAction
		from actions import *
		from runner import Runner
		from ev3dev2.unit import STUD_MM
		from robot import Robot
		from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
		from ev3dev2.wheel import EV3EducationSetTire
		from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveDifferential, Motor
		from utils import SensorMap, BluetoothMaster
		from celebrations import *
		from mission import Mission
		«"\n\n"»
		MAC_ADDRESS = '00:1a:7d:da:71:10'  # Mac address via which the Robots connect with bluetooth
		PORT = 4  # Port on which the Robots connect with bluetooth
		«"\n"»
		sensor_map_master = {'tank_drive': MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM),
		                     'measurement_motor': Motor(OUTPUT_B),
		                     'cs_l': ColorSensor('ev3-ports:in1'), 'cs_m': ColorSensor('ev3-ports:in2'),
		                     'cs_r': ColorSensor('ev3-ports:in3'), 'us_b': UltrasonicSensor('ev3-ports:in4')}
		«"\n"»
		def create_runner():
			r = Robot(SensorMap(sensor_map_master), bluetooth=BluetoothMaster(MAC_ADDRESS, PORT))
			
			«FOR m : simulation.missions SEPARATOR "\n"»«MissionToText(m)»«ENDFOR»
			
			Runner(r, [«FOR m : simulation.missions SEPARATOR ", "»mission_«m.name»«ENDFOR»]).run()
		«"\n\n"»
		if __name__ == '__main__':
			create_runner()
	'''
	
	def static MissionToText(Mission m)'''mission_«m.name» = Mission(«ActionsToText(m.actions)»«IF (m.celebration !== null)», «CelebrationToText(m.celebration)»«ENDIF»)'''
	
	def static ActionsToText(List<Action> acts)'''[«FOR i : 0 ..< acts.size() SEPARATOR ", "»«ActionToText(acts.get(i), acts.size() - i)»«ENDFOR»]'''
	
	def static ActionToText(Action action, int default_prio)'''«ActionTypeToString(action.type)»priority=«PriorityToText(action.priority, default_prio)»)'''
	
	def static String ActionTypeToString(ActionType actionType) {
		if (actionType instanceof BorderAction) return "BorderAction(" + RotationToText((actionType as BorderAction).rotation);
		if (actionType instanceof CollisionAction) return "CollisionAction(" + RotationToText((actionType as CollisionAction).rotation);
		if (actionType instanceof ColorDetAction) return "ColorDetAction(colors=" + ColorsToText((actionType as ColorDetAction).colors) + ", ";
		if (actionType instanceof DriveAction) return "DriveAction(" + SpeedToText((actionType as DriveAction).speed);
		if (actionType instanceof UltrasoundAction) return "UltrasoundAction(" + RotationToText((actionType as UltrasoundAction).rotation) + DodgeRocksToText((actionType as UltrasoundAction).dodgeRocks);
		if (actionType instanceof DontDrownAction) return "DontDrownAction(lakes=" + ColorsToText((actionType as DontDrownAction).colors) + ", " + RotationToText((actionType as DontDrownAction).rotation);
		if (actionType instanceof MeasureAction) return "MeasureAction(colors=" + ColorsToText((actionType as MeasureAction).colors) + ", ";
		if (actionType instanceof PushRockAction) return "PushRockAction(number_of_rocks=" + (actionType as PushRockAction).nr_rocks + ", ";
	}
	
	def static String RotationToText(Rotation r) {
		if (r !== null) {
			return "rotate_degrees=" + r.rotation + ", ";	
		}
		return "";
	}
		
	def static String SpeedToText(Speed s) {
		if (s !== null) {
			return "speed=" + s.speed + ", ";	
		}
		return "";
	}
	
	def static String DodgeRocksToText(Boolean b) {
		if (b == Boolean.FALSE) {
			return "dodge_rocks=False, ";	
		}
		return "";
	}
	
	def static String ColorsToText(List<Color> colors) {
		var res = "[" + ColorToText(colors.get(0));
		for (var i = 1; i < colors.size(); i ++) res += ", " + ColorToText(colors.get(i));
		return res += "]";
	}
	
	def static String ColorToText(Color color) {
		return "ColorSensor.COLOR_" + color.toString().toUpperCase();
	}
	
	def static PriorityToText(Priority priority, int default_prio)'''«IF (priority === null)»«default_prio»«ELSE»«priority.priority»«ENDIF»'''
	
	def static CelebrationToText(Celebration celeb)'''«IF (celeb instanceof DanceCelebration)»DanceCelebration()«ELSE»SpeakCelebration('«(celeb as SpeakCelebration).toSpeak.replace("'", "\\'")»')«ENDIF»'''
}
