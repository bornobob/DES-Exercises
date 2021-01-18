import threading
from utils.bluetoothmessage import BluetoothMessage
from utils.data import Data


class Bluetooth:
    """
    Bluetooth is only there so that other instances of Bluetooth can override it.
    Bluetooth instances are either a master or slave in the bluetooth connection. A master has a server socket to which
    a slave connects. Messages can then be sent between the master and slave. Hence the master sets a server socket
    in the connect() function, and waits to accept another socket (from the slave) for its connection. The slave merely
    needs to connect to the master in the connect() function.
    """
    def __init__(self, server_mac, port=3):
        """
        Initializer for a bluetooth connection, either as slave or master.
        :param server_mac: Address of the device which to connect to.
        :param port: The port via which to connect to the device.
        """
        self.server_mac = server_mac
        self.port = port
        self.database = Data()
        self.socket = None
        self.out_sock = None
        self.in_sock = None

    def get_database(self):
        """
        Gets the database of the bluetooth class.
        """
        return self.database
        

    def disconnect(self):
        """
        Closes all the sockets.
        """
        for s in [self.socket, self.in_sock, self.out_sock]:
            s.close()

    def listen(self):
        """
        Listens to incoming messages on a socket. Puts the message in a database.
        """
        while True:
            message = self.in_sock.readline()
            self.database.put(BluetoothMessage.read_message(message))

    def write(self, message):
        """
        Sends a message through the socket via bluetooth.
        :param message: The BluetoothMessage to be sent over bluetooth.
        """
        self.out_sock.write(str(message) + '\n')
        self.out_sock.flush()

    def connect(self):
        """
        Connects via bluetooth by opening the sockets. Master and slaves can connect if the sockets correspond.
        """
        return None, None, None

    def initiate_connection(self):
        """
        Initiates the bluetooth connection as master or slave. Creates a separate thread to listen to incoming messages.
        """
        self.socket, self.in_sock, self.out_sock = self.connect()
        listener = threading.Thread(target=self.listen)
        listener.start()
