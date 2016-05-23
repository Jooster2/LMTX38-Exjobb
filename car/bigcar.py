from time import sleep
from syslog import syslog
from threading import Lock
from time import sleep
import RPi.GPIO as GPIO

from pololu_drv8835_rpi import motors, MAX_SPEED
from car import Car
import wifihelper

class BigCar(Car):

    def __init__(self):
        self.wh = wifihelper.wifi_helper ()
        wiringpi.pinMode(3, wiringpi.GPIO.OUTPUT)
        wiringpi.digitalWrite (3,1)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)
        self.pwm_steer = GPIO.PWM(18,50)
        self.pwm_steer.start(5)
        self.pwm_pan = GPIO.PWM(21,50)
        self.pwm_pan.start(5)
        self.pwm_tilt = GPIO.PWM(26,50)
        self.pwm_tilt.start(5)

    def drive(self, speed):
        """
            Sets the direction and speed that the car should be driven.
        This is received from wifi_helper. Max speed is 480 which is forward,
        -480 is reverse. 
        """
        print ("IN DRIVE ", speed) 
        self.speed =int((float(speed)/100) * MAX_SPEED)
        print ("IN DRIVE, AFTER CALC", self.speed)
        motors.motor1.setSpeed(self.speed)

    def turn(self,direction, msg):
        """
        Turns the car to either left or right
        Called from wifihelper      
        """
        if direction == "LEFT":
            msg = float (msg)  
            self.pwm_steer.ChangeDutyCycle(7.25 -(((msg-384)/100)*4.0))
            #motors.motor2.setSpeed(MAX_SPEED)

        elif direction == "RIGHT" :
            msg = float (msg)
            self.pwm_steer.ChangeDutyCycle((((msg-128)/100)*4.0)+ 7.25)

            #motors.motor2.setSpeed(-MAX_SPEED)
        else:    
            self.pwm_steer.ChangeDutyCycle(7.25)
           # motors.motor2.setSpeed(0)
        
    def pan (self, direction, msg):
        """
        Calculated for blue servo
        """
        msg = msg-512
        if direction == "LEFT":
            msg = float (msg)
            self.pwm_pan.ChangeDutyCycle((((msg-256)/100)*4.75) + 7.25)
        elif direction == "RIGHT" :
            msg = float (msg)
            self.pwm_pan.ChangeDutyCycle(7.25- (((msg)/100)*4.75))

    def tilt (self, direction, msg):
        
        msg = msg-512
        if direction == "LEFT":
            msg = float (msg)
            self.pwm_tilt.ChangeDutyCycle((((msg-384)/100)*4.0) + 7.25)
        elif direction == "RIGHT" :
            msg = float (msg)
            self.pwm_tilt.ChangeDutyCycle(7.25- (((msg-128)/100)*3.8))

    def special(self, msg):
        """Handles the special capability."""
        if  1024 > msg >= 896:
            self.tilt("LEFT", msg)
            motors.motor2.setSpeed(MAX_SPEED)
        
        elif 896 > msg >= 768:
            self.pan("LEFT",msg)
            motors.motor2.setSpeed(MAX_SPEED)

        elif 768 > msg >= 640:
            self.tilt("RIGHT", msg)
            motors.motor2.setSpeed(MAX_SPEED)

        elif 640 > msg >= 512:
            self.pan("RIGHT", msg)
            motors.motor2.setSpeed(MAX_SPEED)

        return 0
