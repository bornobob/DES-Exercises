from utils.bluetooth import Bluetooth
import bluetooth


class BluetoothSlave(Bluetooth):
    """
    The BluetoothSlave attempts to connect to a server socket from master to establish a bluetooth connection.
    """
    def __init__(self, server_mac, port):
        Bluetooth.__init__(self, server_mac, port)
        self.is_master = False

    def connect(self):
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((self.server_mac, self.port))
        return sock, sock.makefile('r'), sock.makefile('w')
