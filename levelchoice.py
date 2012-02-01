class LevelChoice:
    def select(self):
        pass
    
    
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
        if pygame.font:
            font = pygame.font.Font(None, 18)
            shared.canvas.blit(name, (30, 50*self.index))
        
        
    def select(self):
        pass
