import pygame

import shared
import objects
from vec2d import Vec2d

# the user's interface to the Ball
class Ball:
    def getPos(self):
        return Vec2d(objects.proxy_map[self].getPos())
        
# the internal Ball object
class _Ball:
    proxy_type = Ball
    
    def __init__(self, pos):
        self.radius = 10
        self.pos = pos
        self.vel = Vec2d(100,100)
        
    def getPos(self): #make sure to return a copy
        return self.pos
        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        self.pos += self.vel * elapsed
        if self.pos.x > shared.dim.x - self.radius or self.pos.x < self.radius:
            self.vel.x *= -1
        if self.pos.y > shared.dim.y - self.radius or self.pos.y < self.radius:
            self.vel.y *= -1
        
    def draw(self):
        # we're a little blue circle
        loc = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(shared.canvas, (30, 30, 200), loc, self.radius)
