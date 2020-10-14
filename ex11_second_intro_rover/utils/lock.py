class Lock:
    def __init__(self):
        self.value = False

    def is_locked(self):
        print('checking lock')
        return self.value

    def lock(self):
        self.value = True

    def unlock(self):
        self.value = False
