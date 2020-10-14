import bluetooth, threading
from time import sleep
from utils.Bluetooth import Bluetooth


class BluetoothMaster(Bluetooth):

    def __init__(self, server_mac):
        Bluetooth.__init__(self, server_mac)
        self.is_master = True

    def connect(self):
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind((self.server_mac, self.port))
        server_sock.listen(1)
        print('Listening...')
        client_sock, address = server_sock.accept()
        print('Accepted connection from ', address)
        return client_sock, client_sock.makefile('r'), client_sock.makefile('w')

    def run(self):
        sock, sock_in, sock_out = self.connect()
        listener = threading.Thread(target=self.start_listening, args=(sock_in, sock_out))
        listener.start()
        i = 0
        while i < 20:
            print('[' + str(i) + '] Doing something...')
            sleep(1)
            i += 1
        self.disconnect(sock_in)
        self.disconnect(sock_out)
        self.disconnect(sock)

    def start_listening(self, sock_in, sock_out):
        i = 1
        sock_out.write(str(i) + '\n')
        sock_out.flush()
        print('Sent ' + str(i))
        self.listen(sock_in, sock_out)
