from ev3dev2.sensor.lego import UltrasonicSensor


class SensorMap:
    """
    Class to map sensors to ports
    """
    def __init__(self, mapping):
        self.mapping = mapping
        self.configure_sensors()

    def configure_sensors(self):
        for v in self.mapping.values():
            if isinstance(v, UltrasonicSensor):
                v.mode = UltrasonicSensor.MODE_US_DIST_CM

    def __getattr__(self, attr):
        return self.mapping[attr]
