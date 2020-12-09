class Data:
    """
    Database for sensory data
    """
    def __init__(self):
        """
        Initializer of the Data class. Gives it an empty dictionary to keep its data in.
        """
        self.data = {}
    
    def put(self, btmsg):
        """
        Puts the contents of a BluetoothMessage in the dictionary of the Data object.
        :param btmsg: The BluetoothMessage is put into the Data dictionary
        """
        self.data[btmsg.key] = float(btmsg.value)

    def __getattr__(self, item):
        """
        Obtains the value of the corresponding key (item) in the Data object its dictionary.
        :param item: The key in the Data object from which we want to obtain the value.
        """
        try:
            return self.data[item]
        except KeyError:
            return None
