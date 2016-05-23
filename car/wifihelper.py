import socket
import syslog
from threading import Thread
from threading import Lock
import collections
import wiringpi
import urllib2
class wifi_helper:
    """
    Handles the WiFI connection, receiving and sending data. 
    The data sent is feedback from device, the data received is
    instructions top the device.
    """
    
    def __init__ (self):
        wiringpi.pinMode(19, wiringpi.GPIO.OUTPUT)
        self.start_thread()
    def start_thread(self):
        self.thread = Passive_thread()
        self.thread.daemon = True
        self.thread.set_wh(self)
        self.active = Active_thread()
        self.active.daemon = True
        self.active.start()
        self.thread.start()

"""



def internet_on():
    try:
        print "INTERNET ON"
        answer = urllib2.urlopen('http://74.125.228.100', timeout=1)
        return True
    except urllib.URLError as err: pass
    return False
"""
class Passive_thread(Thread):
    def __init__ (self):
        Thread.__init__(self)
        print ("In init")
        self.has_data = False
        self.data = collections.deque()
    def set_wh (self,wh):
        self.wh = wh

    def run(self):
        try: 
            s = socket.socket()
            port = 50007
            print ("In run, socket created")
            s.bind(('',port))

            print ("In after bind")
            s.listen(5)
            while True:
                syslog.syslog (syslog.LOG_INFO,"In while, before socket accept")
                wiringpi.digitalWrite(19, 1)
                """

                if internet_on():
                    wiringpi.digitalWrite(19, 1)
                    """
                c, addr = s.accept()
                print ("In while, socket accepted")
                connected = True
                #'c' is a newly create socket usable for write
                #and read on connection. addr is client addr,
                #bound to socket.
                wiringpi.digitalWrite(19, 0)
                syslog.syslog (syslog.LOG_INFO,'Got connection from '+ str(addr))
                self.wh.active.set_connection (c)
                while connected:
                    msg_size =c.recv(1)
                    print "The size: ", msg_size
                    if not msg_size:
                        connected = False
                    else:
                        msg_size = int (msg_size)
                        if msg_size == 1:
                            msg = int(c.recv (1))
                            print ("When size is 1: ", msg)
                        elif msg_size == 2:
                            msg = int(c.recv(2))
                            print ("When size is 2: ", msg)
                        elif msg_size == 3:
                            msg = int(c.recv(3))
                            print ("When size is 3: ", msg)
                        elif msg_size == 4:
                            msg = int (c.recv(4))
                            print ("When size is 4: ", msg)
                    if connected:
                        self.data.append(int (msg))
                        #print ("msg received")
                        self.has_data = True
                #Receiving size should be fixed
               # msg = s.recv()
               # c.close()
               # c.send ("HEJ".encode())
                
               # car.receive_data (msg)
        except socket.error as e:
            print(e)


class Active_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        print ("In active init")
        self.lock = Lock()
        self.queue = collections.deque()
    
    def start_active(self):
        self.start()
    
    def set_connection(self, conn):
        self.conn = conn
    
    def add_element(self, data):
        self.queue.append(data)
        if self.lock.locked():
            self.lock.release()

    def run(self):
        while True:
            if self.queue:
                print ("Removing items from queue")
                self.conn.send(self.queue.popleft().encode())
            else:
                
                print ("Empty queue")
                self.lock.acquire()
                
                print ("Empty queue after lock")

#wh = wifi_helper()
#wh.thread.active.add_element(24)
#wh.thread.active.add_element(54)
#wh.thread.active.start_active()

#while True:
 #   x = input()
  #  wh.thread.active.add_element(x)
    
