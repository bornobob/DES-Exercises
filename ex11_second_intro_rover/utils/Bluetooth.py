from time import sleep


class Bluetooth:

    def __init__(self, server_mac, port=3):
        self.server_mac = server_mac
        self.port = port

    @staticmethod
    def disconnect(sock):
        sock.close()

    @staticmethod
    def listen(sock_in, sock_out):
        print('Now listening...')
        while True:
            data = int(sock_in.readline())
            print('Received ' + str(data))
            data += 1
            sleep(1)
            sock_out.write(str(data) + '\n')
            sock_out.flush()
            print('Sent ' + str(data))
