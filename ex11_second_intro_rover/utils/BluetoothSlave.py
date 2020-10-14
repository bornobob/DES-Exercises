import bluetooth, threading
from time import sleep
from utils.Bluetooth import Bluetooth


class BluetoothMaster(Bluetooth):

    def __init__(self, server_mac):
        Bluetooth.__init__(self, server_mac)
        self.is_master = False

    def connect(self):
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('Connecting...')
        sock.connect((self.server_mac, self.port))
        print('Connected to ', self.server_mac)
        return sock, sock.makefile('r'), sock.makefile('w')

    def run(self):
        sock, sock_in, sock_out = self.connect()
        listener = threading.Thread(target=self. listen, args=(sock_in, sock_out))
        listener.start()
        i = 0
        while i < 20:
            print('[' + str(i) + '] Doing something...')
            sleep(1)
            i += 1
        self.disconnect(sock_in)
        self.disconnect(sock_out)
        self.disconnect(sock)
