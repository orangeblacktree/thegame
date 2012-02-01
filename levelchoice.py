class LevelChoice:
    def select(self):
        objects.proxy_map[self].select()
    
    
class _LevelChoice:
    proxy_type = LevelChoice

    def __init__(self, index, name):
        self.index = index
        self.name = name
        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        pass
        
    def select(self):
        pass