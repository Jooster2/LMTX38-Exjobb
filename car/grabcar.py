from time import sleep
import syslog

from pololu_drv8835_rpi import motors, MAX_SPEED
from car import Car
import wiringpi
import wifihelper

class GrabCar(Car):
    def __init__(self):
        syslog.syslog(syslog.LOG_INFO, "Initializing GrabCar")
        self.wh = wifihelper.wifi_helper ()
        wiringpi.pinMode(3, wiringpi.GPIO.OUTPUT)
        wiringpi.digitalWrite (3,1)

    def special(self, msg):
        """Activate the magnet."""
        syslog.syslog(syslog.LOG_INFO, "Magnet activated")
        #TODO implement magnet usage
        return msg

    def deactivate_special(self):
        syslog.syslog(syslog.LOG_INFO, "Magnet deactivated")
        pass

    def drive(self, speed):
        """
            Sets the direction and speed that the car should be driven.
        This is received from wifi_helper. Max speed is 480 which is forward,
        -480 is reverse. 
        """
        self.speed = int((float(speed)/100) * MAX_SPEED)
        motors.motor1.setSpeed(self.speed)

    def turn(self, direction, msg):
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


