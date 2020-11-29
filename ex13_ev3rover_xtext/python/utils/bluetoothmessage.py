class BluetoothMessage:
    """
    A simple Bluetooth Message carrying a key and value
    """
    def __init__(self, key, value):
        """
        The initializer of the BluetoothMessage class.
        :param key: The key that indexes the motors and sensors.
        :param value: The value ascribed to the key.
        """
        self.key = key
        self.value = value

    def __str__(self):
        """
        Overwrites the standard __str__ method with the key and value pair of the BluetoothMessage class.
        """
        return '{0:}:{1:}'.format(self.key, self.value)

    @classmethod
    def read_message(cls, data):
        """
        Creates an object with the data in a BluetoothMessage, creating a new BluetoothMessage.
        :param data:
        """
        return cls(*data.split(':'))
