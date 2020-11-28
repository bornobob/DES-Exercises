class BluetoothMessage:
    """
    A simple Bluetooth Message carrying a key and value
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return '{0:}:{1:}'.format(self.key, self.value)

    @classmethod
    def read_message(cls, data):
        return cls(*data.split(':'))
