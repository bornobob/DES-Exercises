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
        Checks if the lock is locked.
        :return: True if the lock is locked, False otherwise.
        """
        return self.value

    def lock(self):
        """
        Locks the lock.
        """
        self.value = True

    def unlock(self):
        """
        Unlocks the lock.
        """
        self.value = False
