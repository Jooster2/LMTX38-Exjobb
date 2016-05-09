import PIL
from collections import deque
from threading import Thread
from threading import Lock

class ImageTransmitter:
    """Used to transfer images over a socket."""

    def __init__(self, socket):
        self.socket = socket
        self.queue = deque()
        self.connected = True
        self.queue_lock = Lock()

    def add_image(self, image):
        """Add the image to queue."""
        thread = Thread(target=self.append, args=(image,))
        thread.start()

    def append(self, image):
        """
        Converts image to bytes and add to queue. Never call
        outside ImageTransmitter.
        """
        self.queue_lock.acquire()
        print("lock acquired in append")
        self.queue.append(image.tobytes())
        self.queue_lock.release()
        print("lock released in append")
        
    def send(self):
        """
        Send images over the socket. 
        amount -- how many images to send. Defaults to -1 which 
        means send until queue is empty.
        """
        thread = Thread(target=self.send_thread)
        thread.start()


    def send_thread(self):
        """
        Send image over the socket. Never call outside
        ImageTransmitter.
        """
        self.queue_lock.acquire()
        print(self.queue.popleft())
        self.queue_lock.release()
