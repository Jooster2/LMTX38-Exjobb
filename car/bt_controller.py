from threading import Thread
from collections import deque
import bluetooth



class BtController:
    """
    Creates and manages connections over Bluetooth.
    """

    def __init__(self):
        self.server_socket = bluetooth.BlueToothSocket()
        self.data = deque(50)
        Thread(target=self.listen).start()
        self.active = None
        self.passive = None


    def listen(self):
        """
        Listen for new connections, and establish a new
        active connection if there is none. If there is,
        ask the user to change.
        """

        self.server_socket.bind("", 0)
        self.server_socket.listen(3)
        while True:
            socket, addr = self.server_socket.accept()
            if self.active and self.active.is_active:
                self.change_player(socket)
            else:
                self.active = ActiveConnection(socket)


    def change_player(self, socket):
        """Handle a request to change player."""
        pass 
            

class ActiveConnection:
    """Handles sending and receiving data to the player."""

    def __init__(self, socket):
        self.socket = socket
        self.data_received = collections.deque(50)
        self.recv = Thread(target=recv_thread)
        self.is_active = True

        
    def get_data(self):
        """Remove and return the oldest data in the deque."""
        return self.data_received.pop()
    
    def send(self, data):
        """Start a send_thread and send the data."""
        Thread(target=send_thread, args=data)

    def recv_thread(self):
        """Receives data and handles it."""
        while self.socket:
            data_size = self.socket.recv(1)
            data = (self.socket.recv(int(data_size)))
            # format data
            if data == ascii.EOT:
                self.socket.close()
                self.is_active = False
                break
            self.data_received.appendleft(data)

    def send_thread(self, data):
        """Send data to socket."""
        self.socket.send(data)





