class Lock:
    """

    """
    def __init__(self):
        """
        Initializer for a lock.
        """
        self.value = False

    def is_locked(self):
        """

        :return:
        """
        return self.value

    def lock(self):
        self.value = True

    def unlock(self):
        self.value = False
