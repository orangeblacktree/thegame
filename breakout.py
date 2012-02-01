# ------------------------------------------------------------------
# breakout.py
# 
# Player!
# ------------------------------------------------------------------

import pygame

import shared
import userspace
import objects
from vec2d import Vec2d

# some settings
move_speed = 200

class Breakout:
    def __init__(self):
        p = objects.create(_Paddle, Vec2d(int(shared.dim.x/2), int(shared.dim.y - 20)))
        b = objects.create(_Ball, Vec2d(shared.dim) / 2)
        bricks = {}
        for row in xrange(0, 10):
            for col in xrange(0, int(shared.dim.x/40)):
                brick = objects.create(_Brick, Vec2d(40,20)*(col,row) + (5,5))
                bricks[(row, col)] = brick.proxy
                
        userspace.space['bricks'] = bricks
        userspace.space['ball'] = b.proxy
        userspace.space['paddle'] = p.proxy

class Brick:
    def getPos(self):
        return objects.proxy_map[self].getPos()
        
class _Brick:
    proxy_type = Brick
    
    def __init__(self, pos):
        self.pos = pos
        self.broken = False
        
    def getPos(self):
        return pos
        
    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        loc = (int(self.pos.x), int(self.pos.y), 38, 18)
        pygame.draw.rect(shared.canvas, (255, 0, 0), loc)
        
# the user's interface to the Ball
class Ball:
    def getPos(self):
        return objects.proxy_map[self].getPos()
        
# the internal Ball class
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
        # collide
        
    def draw(self):
        # we're a little blue circle
        loc = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(shared.canvas, (30, 30, 200), loc, self.radius)
        
# the user's interface to the Paddle
class Paddle:
    def getPos(self):
        return objects.proxy_map[self].getPos()

    def move(self, direction):
        vel = {
            "left" : Vec2d(-move_speed, 0),
            "right" : Vec2d(move_speed, 0),
        }[direction]
        objects.proxy_map[self].walk(0.2, vel)

# the internal Paddle object
class _Paddle:
    proxy_type = Paddle

    def __init__(self, pos):
        self.pos = pos
        self.vel = Vec2d(0, 0)

        # not walking yet
        self.walking = False

    def destroy(self):
        pass

    def step(self, elapsed):
        # ds = v dt
        self.pos += self.vel * elapsed

        # walk timing
        if self.walking:
            self.walk_timer -= elapsed
            if self.walk_timer <= 0:
                self.vel = Vec2d(0, 0)
                self.walking = False

    def draw(self):
        # we're a little red rectangle
        rect = pygame.Rect(self.pos.x, self.pos.y, 40, 10)
        pygame.draw.rect(shared.canvas, (255, 0, 0), rect)

    def getPos(self): #make sure to return a copy
        return self.pos
        
    def walk(self, time, vel):
        # start walking if not walking already
        #if not self.walking:
            self.walking = True
            self.walk_timer = time
            self.vel = vel
