import pygame

import shared
import objects
from vec2d import Vec2d

class Brick:
    def getPos(self):
        return objects.proxy_map[self].getPos()
        
class _Brick:
    proxy_type = Brick
    
    def __init__(self, pos):
        self.pos = pos
        self.dim = Vec2d(40,20)
        self.broken = False
        
    def getPos(self):
        return pos
        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        if not self.broken:
            loc = (int(self.pos.x), int(self.pos.y), 38, 18)
            pygame.draw.rect(shared.canvas, (255, 0, 0), loc)
