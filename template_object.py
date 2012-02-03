# object interface visible to user code
class Object:
    pass
# internal object
class _Object:
    proxy_type = Object

    def __init__(self, proxy):
        self.proxy = proxy
        pass

    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        pass
