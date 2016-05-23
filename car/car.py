#!/usr/bin/python2

from time import sleep
from syslog import syslog
import socket

import wifihelper
import wiringpi
from pololu_drv8835_rpi import motors, MAX_SPEED

class Car:
    """
    Class that handles the driving of the car and its special 
    capabilities.
    """
        
    def special(self, msg):
        raise NotImplementedError("Method not in subclass.")

        
    def receive_data (self, msg):
        """
        Receives data and decides what to do with it.
        """
        msg = int (msg)
        if msg > 512:
            msg = special(msg)

        if  512 > msg >= 384:
            self.turn ("LEFT", msg)
        elif 384 > msg >= 256:
          #  print ("When size is 2 we end up here: ")
            self.drive (-(msg-256))
        elif 256 > msg >= 129:
            self.turn ("RIGHT", msg)
        elif 128 == msg: 
            self.turn (1, msg)
        elif 128 > msg:
            self.drive (msg)
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
    elif hostname == "grabcar":
        car = GrabCar()
    elif hostname == "camcar":
        car = CamCar()
    else:
        raise ValueError("Hostname is wrong use one of \
                bigcar/grabcar/camcar.")
    run(car)

