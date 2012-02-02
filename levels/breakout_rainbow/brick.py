import pygame

import shared
import objects
from vec2d import Vec2d
from random import randint

# the user's interface to the Brick
class Brick:
    def getPos(self):
        return Vec2d(objects.proxy_map[self].getPos())
        
# the internal Brick object
class _Brick:
    proxy_type = Brick
    
    def __init__(self, pos):
        self.pos = pos
        self.dim = Vec2d(38,18)
        self.broken = False
        self.col = (randint(0, 255), randint(0, 255), randint(0, 255))
        
    def getPos(self):
        return pos
        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        if not self.broken:
            loc = (int(self.pos.x), int(self.pos.y), 38, 18)
            pygame.draw.rect(shared.canvas, self.col, loc)
