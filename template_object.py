# interface visible to user code
class Object:
    pass

# internal object
class _Object:
    def __init__(self):
        pass

    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        pass
