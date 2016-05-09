from camera import Camera
from time import sleep
cam = Camera(None)
cam.start()

sleep(2)
cam.active = False

