from queue import Queue
import threading


class Bluetooth:
    def __init__(self, server_mac, port=3):
        self.server_mac = server_mac
        self.port = port
        self.queue = Queue()
        self.socket = None
        self.out_sock = None
        self.in_sock = None

    def disconnect(self):
        for s in [self.socket, self.in_sock, self.out_sock]:
            s.close()

    def listen(self):
        while True:
            color = int(self.in_sock.readline())
            self.queue.put(color)

    def write(self, data):
        self.out_sock.write(str(data) + '\n')
        self.out_sock.flush()

    def connect(self):
        return None, None, None

    def initiate_connection(self):
        self.socket, self.in_sock, self.out_sock = self.connect()
        print('after connect:', self.socket, self.in_sock, self.out_sock)
        listener = threading.Thread(target=self.listen)
        listener.start()
