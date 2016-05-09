import PIL
from collections import deque
from threading import Thread
from threading import Lock

class ImageTransmitter:
    """Used to transfer images over a socket."""

    def __init__(self, socket):
        self.socket = socket
        self.queue = Deque(5)
        self.connected = True
        self.queue_lock = Lock()

    def add_image(self, image):
        """Add the image to queue."""
        thread = Thread(target=append, args=image)
        thread.start()

    def append(self, image):
        """
        Converts image to bytes and add to queue. Never call
        outside ImageTransmitter.
        """
        self.queue_lock.acquire()
        self.queue.append(image.tobytes())
        self.queue_lock.release()
        
    def send(self, amount=-1):
        """
        Send images over the socket. 
        amount -- how many images to send. Defaults to -1 which 
        means send until queue is empty.
        """
        if amount == 0:
            raise ValueError("Amount specified is 0, intentional?")
        else:
            thread = Thread(target=send_thread, args=amount)
            thread.start()


    def send_thread(self, amount=-1):
        """
        Send image over the socket. Never call outside
        ImageTransmitter.
        """
        count = 0
        while self.queue:
            self.queue_lock.acquire()
            self.socket.send(len(self.queue[0]))
            self.socket.send(self.queue.popleft())
            self.queue_lock.release()
            count += 1
            if count >= amount and amount > 0:
                break

