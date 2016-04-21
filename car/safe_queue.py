from collections import deque
class Safe_Queue(deque):
    
    def __init__ (self):
        deque.__init__(self)
        self.lock = Lock()

    
    def add_element(self, data):
        self.append(data)
        if self.lock.locked():
            self.lock.release()
    
    def get_element(self):
        self.popleft()

