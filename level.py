class Level:
    def __init__(self):
        self.completed = False

    def start(self):
        pass

    def stop(self):
        pass
        
    def getState(self):
        pass
        
    def restoreState(self, state):
        pass
        
    def event(self, event):
        pass

    def step(self, elapsed):
        pass
