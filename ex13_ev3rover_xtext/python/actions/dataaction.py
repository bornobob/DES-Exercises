from actions.baseaction import BaseAction
import time
from utils import BluetoothMessage

class DataAction(BaseAction):
    """
    """
    def __init__(self, priority, polling_rate=100):
        super().__init__(priority)
        self.touch_b_start = False
        self.touch_l_start = False
        self.touch_r_start = False
        self.start_time = time.time()
        self.polling_rate = polling_rate

    def check(self):
        return self.robot.sensormap.ts_b.is_pressed != self.touch_b_start or \
               self.robot.sensormap.ts_l.is_pressed != self.touch_l_start or \
               self.robot.sensormap.ts_r.is_pressed != self.touch_r_start or \
               (time.time() - self.start_time) * 1000 >= self.polling_rate

    def _do_action(self):
        if self.robot.sensormap.ts_b.is_pressed != self.touch_b_start:
            self.robot.bluetooth.write(
                BluetoothMessage('ts_b', self.robot.sensormap.ts_b.is_pressed))
            self.touch_b_start = self.robot.sensormap.ts_b.is_pressed
        elif self.robot.sensormap.ts_l.is_pressed != self.touch_l_start:
            self.robot.bluetooth.write(
                BluetoothMessage('ts_l', self.robot.sensormap.ts_l.is_pressed))
            self.touch_l_start = self.robot.sensormap.ts_l.is_pressed
        elif self.robot.sensormap.ts_r.is_pressed != self.touch_r_start:
            self.robot.bluetooth.write(
                BluetoothMessage('ts_r', self.robot.sensormap.ts_r.is_pressed))
            self.touch_r_start = self.robot.sensormap.ts_r.is_pressed
        elif (time.time() - self.start_time) * 1000 >= self.polling_rate:
            self.robot.bluetooth.write(
                BluetoothMessage('us_f', self.robot.sensormap.us_f.value()))
            self.start_time = time.time()
