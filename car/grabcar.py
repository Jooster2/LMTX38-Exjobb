from time import sleep
from syslog import syslog
from pololu_drv8835_rpi import motors, MAX_SPEED
import wifihelper
from threading import Lock
from time import sleep
import wiringpi
from car import Car

class GrabCar(Car):
    def __init__(self):
        self.wh = wifihelper.wifi_helper ()
        wiringpi.pinMode(3, wiringpi.GPIO.OUTPUT)
        wiringpi.digitalWrite (3,1)

    def drive(self, speed):
        """
            Sets the direction and speed that the car should be driven.
        This is received from wifi_helper. Max speed is 480 which is forward,
        -480 is reverse. 
        """
        self.speed = int((float(speed)/100) * MAX_SPEED)
        motors.motor1.setSpeed(self.speed)

    def turn(self, direction):
        """
        Turns the car to either left or right
        Called from wifihelper
        """
        if direction == "LEFT":
            motors.motor2.setSpeed(MAX_SPEED)

        elif direction == "RIGHT" :
            motors.motor2.setSpeed(-MAX_SPEED)
        else:
            motors.motor2.setSpeed(0)


