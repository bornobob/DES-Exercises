import bluetooth
from utils.bluetooth import Bluetooth


class BluetoothMaster(Bluetooth):
    def __init__(self, server_mac, port):
        Bluetooth.__init__(self, server_mac, port)
        self.is_master = True

    def connect(self):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind((self.server_mac, self.port))
        server_sock.listen(1)
        client_sock, address = server_sock.accept()
        return client_sock, client_sock.makefile('r'), client_sock.makefile('w')
