import pygame

import shared
import objects
from vec2d import Vec2d

# the user's interface to the Brick
class Brick:
    def getPos(self):
        return Vec2d(objects.proxy_map[self].getPos())
        
# the internal Brick object
class _Brick:
    proxy_type = Brick
    
    def __init__(self, pos):
        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        self.width = pos.width
        self.height = pos.height
        self.broken = False
        
    def getPos(self):
        return pos
        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        if not self.broken:
            pygame.draw.rect(shared.canvas, (255, 0, 0), self.pos)
