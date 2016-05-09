from PIL import Image
import io
from picamera import PiCamera
from threading import Thread
from time import time, sleep

from image_transmitter import ImageTransmitter

class Camera(Thread):
    
    def __init__(self, socket, latency=66.67):
        """
        Constructor
        socket -- the socket to transmit images over
        latency -- the time between each image capture, defaults
        to 66.67ms, which is rougly equal to 15 FPS
        """
        super().__init__()
        self.transmitter = ImageTransmitter(socket)
        self.camera = PiCamera()
        self.active = False
        self.latency = latency

    def run(self):
        self.active = True
        stream = io.BytesIO()
        while self.active:
            print("entering while-loop")
            start = time()
            self.camera.capture(stream, format="jpeg", quality=10)
            stream.seek(0)
            self.transmitter.add_image(Image.open(stream))
            self.transmitter.send()
            print((self.latency - (time()-start))/1000)
            sleep((self.latency - (time()-start))/1000)

        stream.close()

        

