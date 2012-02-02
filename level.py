# ------------------------------------------------------------------
# level.py
# 
# Base class for level 'Main' classes
# ------------------------------------------------------------------

class Empty:
    pass

class Level:
    def __init__(self):
        self.data = Empty()
        self.data.completed = False

    def start(self):
        pass

    def stop(self):
        pass
        
    def event(self, event):
        pass

    def step(self, elapsed):
        pass
