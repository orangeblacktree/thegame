import pygame

import shared
import objects
from vec2d import Vec2d

# the user's interface to the Ball
class Ball:
    def getPos(self):
        return objects.proxy_map[self].getPos()
        
# the internal Ball class
class _Ball:
    proxy_type = Ball
    
    def __init__(self, pos, bricks, paddle):
        self.radius = 10
        self.pos = pos
        self.vel = Vec2d(100,100)
        self.bricks = bricks
        self.paddle = paddle
        
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
            
        # collide
        for loc in self.bricks:
            brick = self.bricks[loc]
            if brick.broken:
                continue
            if ((self.pos.y > brick.pos.y - self.radius and self.pos.y <  brick.pos.y + brick.dim.y + self.radius) and
               (self.pos.x > brick.pos.x - self.radius and self.pos.x <  brick.pos.x + brick.dim.x + self.radius)):
                brick.broken = True
                if self.pos.x > brick.pos.x+brick.dim.x or self.pos.x < brick.pos.x:
                    self.vel.y *= -1
                if self.pos.y > brick.pos.y+brick.dim.y or self.pos.y < brick.pos.y:
                    self.vel.x *= -1
                    
            if self.pos.y > self.paddle.pos.y - self.radius and self.pos.x > self.paddle.pos.x - self.radius and self.pos.x < self.paddle.pos.x + self.paddle.dim.x + self.radius:
                self.vel.y = -abs(self.vel.y)
                
        
    def draw(self):
        # we're a little blue circle
        loc = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(shared.canvas, (30, 30, 200), loc, self.radius)
