from PIL import Image
import io
from picamera import PiCamera
from threading import Thread
from time import time, sleep

from image_transmitter import ImageTransmitter

class Camera(Thread):
    
    def __init(self, socket, latency=66.67):
        """
        Constructor
        socket -- the socket to transmit images over
        latency -- the time between each image capture, defaults
        to 66.67ms, which is rougly equal to 15 FPS
        """
        self.transmitter = ImageTransmitter(socket)
        self.camera = PiCamera(resolution = (800, 600))
        self.active = False
        self.latency = latency

    def run(self):
        self.active = True
        stream = io.BytesIO()
        self.camera.start_preview()
        sleep(2)
        i = 0
        while self.active:
            start = time()
            self.camera.capture_continuous(stream, format="jpeg", 
                    quality=10)
            stream.seek(0)
            #self.transmitter.add_image(Image.open(stream))
            #self.transmitter.send()
            print(i)
            i += 1
            sleep(latency - (time()-start))

        stream.close()

        

