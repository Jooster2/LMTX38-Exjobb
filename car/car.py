#!/usr/bin/python2

from time import sleep
from syslog import syslog
from time import sleep
import socket

from pololu_drv8835_rpi import motors, MAX_SPEED
import wifihelper
import wiringpi
import RPi.GPIO as GPIO
class Car:
    """
    Class that handles the driving of the car and its special 
    capabilities.
    """
        
    def special(self, msg):
        raise NotImplementedError("Unimplemented method called")

    def receive_data (self, msg):
        """
        Receives data and decides what to do with it.
        """
        msg = int (msg)
        if msg >= 512:
            msg = special(msg)
        elif  512 > msg >= 384:
            self.turn ("LEFT", msg)
            motors.motor2.setSpeed(0)
        elif 384 > msg >= 256:
          #  print ("When size is 2 we end up here: ")
            self.drive (-(msg-256))
            motors.motor2.setSpeed(0)
        elif 256 > msg >= 129:
            self.turn ("RIGHT", msg)
            motors.motor2.setSpeed(0)
        elif 128 == msg:
            self.turn (1, msg)
            motors.motor2.setSpeed(0)
        elif 128 > msg:
            self.drive (msg)
            motors.motor2.setSpeed(0)
           # print ("When size is 1 we end up here: ")

    def send_data(self,data):
        #active.add_element
        pass

def run(car):
    while True:
        sleep(0.01)
        if car.wh.thread.has_data:
            try:
                msg = car.wh.thread.data.popleft()
                car.receive_data(msg)
            except IndexError:
                car.wh.thread.has_data = False

if __name__ == "__main__":
    hostname = socket.gethostname()
    if hostname == "bigcar":
        car = BigCar()
    elif hostname == "camcar":
        car = CamCar()
    elif hostname == "grabcar":
        car = GrabCar()

    run(car)

