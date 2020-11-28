class Data:
    """
    Database for sensory data
    """
    def __init__(self):
        self.data = {}
    
    def put(self, btmsg):
        self.data[btmsg.key] = btmsg.value

    def __getattr__(self, item):
        return self.data[item]
