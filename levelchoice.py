import pygame
import shared
import objects

class LevelChoice:
    def select(self):
        objects.proxy_map[self].select()
    
    
class _LevelChoice:
    proxy_type = LevelChoice

    def __init__(self, index, name):
        self.index = index
        self.name = name
        self.font = pygame.font.Font(None, 64)
        self.text = self.font.render(self.name, 1, (255, 255, 255)) 

        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        if pygame.font:
            shared.canvas.blit(self.text, (30, 50*(1+self.index)))
        
        
    def select(self):
        pass
