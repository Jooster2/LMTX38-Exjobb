from time import sleep
from pololu_drv8835_rpi import motors, MAX_SPEED
import wifihelper

class Car:
    """
    Class that handles the driving of the car and its special 
    capabilities.
    """
    def __init__(self):
        self.wh = wifihelper.wifi_helper ()
        
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


    def turn(self,direction):
        """
        Turns the car to either left or right
        Called from wifihelper
        """
        if direction == "LEFT":
            motors.motor2.setSpeed(MAX_SPEED)

        else :
            motors.motor2.setSpeed(-MAX_SPEED)

        
    def receive_data (self, msg):
        """
        Receives data and decides what to do with it.
        """
        msg = int (msg)
        if  512 >msg > 383:
            self.turn ("LEFT")
        elif 256 > msg >128:
            self.turn ("RIGHT")
        elif 384 > msg >255:
            self.drive (msg-256)
        elif msg < 128:
            self.drive (-msg)

    def send_data(self,data):
        #active.add_element
        pass

car = Car()
while True:
    if car.wh.thread.has_data:
        try:
            msg = car.wh.thread.data.popleft()
            car.receive_data(msg)
        except IndexError:
            car.wh.thread.has_data = False

"""
if __name__ == "__main__":
    car = Car()
    for x in range(0, 100,1):
        y = float (x)
        car.drive(y/100)
        sleep(0.1)


    for x in range(0, -100,-1):
        y = float (x)
        car.drive(y/100)
        sleep(0.1)

    temp = input()
    car.drive(temp)
"""
