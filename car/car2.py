from gpiozero import OutputDevice
from gpiozero import PWMOutputDevice
import time
#from RPIO import PWM
class Car:
    """
    Class that handles the driving of the car and its special 
    capabilities.
    """
    def __init__(self):
        
        self.engine   = OutputDevice(pin = 3)
        self.mode   = OutputDevice(pin = 2)
        self.speed   = PWMOutputDevice(pin = 17, initial_value = 1)

        
        self.engine.on()
        self.mode.on()
        self.drive()
    def drive(self):
        """
            Sets the direction and speed that the car should be driven.
        This is received from wifi_helper.
        """
        """
        GPIO.output(engine, 1)
        PWM.setup()
        PWM.init_channel(0)
        PWM.add_channel_pulse(0,17, 0, 50)
        PWM.add_channel_pulse(0,17, 100, 50)
        time.sleep(5)
        PWM.clear_channel_gpio(0,17)
        PWM.cleanup()
        """
        
        self.speed.on()
        self.speed.blink(on_time = 0.01, off_time = 0.01, fade_in_time = 0.005, fade_in_time = 0.005)
        print ("PWM IS ACTIVE:")
        print (self.speed.is_active)
        print ("PWM value:")
        print (self.speed.value)
        print ("Engine IS ACTIVE:")
        print (self.engine.active_high)
        print ("Engine ValuE:")
        print (self.engine.value)
        print ("mode active:")
        print (self.mode.active_high)
        print ("mode value:")
        print (self.mode.value)
        while True:
           temp=  input ()
           self.speed.close()
           self.speed.on()
           self.blink (on_time = temp, off_time = temp, fade_in_time = 0.005, fade_off_time = 0.005)




    def turn(self,direction):
        """
        Turns the car to either left or right
        Called from wifihelper
        """
        pass
    def receive_data (self, msg):
        """
        Receives data and decides what to do with it.
        """
        if msg == "drive forward":
            #drive forward with specified speed
            #etc etc
            pass
    def send_data(self,data):
        #active.add_element
        pass

car = Car()
