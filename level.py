# ------------------------------------------------------------------
# level.py
# 
# Base class for each state of the game
# ------------------------------------------------------------------

class Level:
    def __init__(self):
        self.deps = []
        self.next_level = 0

    # called when we enter this level, create objects etc.
    def start(self):
        pass

    # called each frame of the level
    def step(self, elapsed):
        pass

    # called when we leave this level, destroy objects etc.
    def stop(self):
        pass

