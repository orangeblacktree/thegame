import pygame

import shared
import objects
from vec2d import Vec2d

# some settings
move_speed = 200

# the user's interface to the Paddle
class Paddle:
    def getPos(self):
        return objects.proxy_map[self].getPos()

    def move(self, direction):
        vel = {
            "left" : Vec2d(-move_speed, 0),
            "right" : Vec2d(move_speed, 0),
        }[direction]
        objects.proxy_map[self].walk(0.05, vel)

# the internal Paddle object
class _Paddle:
    proxy_type = Paddle

    def __init__(self, pos):
        self.pos = pos
        self.dim = Vec2d(40, 10)
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
        rect = pygame.Rect(self.pos.x, self.pos.y, self.dim.x, self.dim.y)
        pygame.draw.rect(shared.canvas, (255, 0, 0), rect)

    def getPos(self): #make sure to return a copy
        return self.pos
        
    def walk(self, time, vel):
        self.walking = True
        self.walk_timer = time
        self.vel = vel
