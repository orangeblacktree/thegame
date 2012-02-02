import pygame

import shared
import objects
from vec2d import Vec2d
import random

# some settings
move_speed = 200

# the user's interface to the Paddle
class Paddle:
    def getPos(self):
        return Vec2d(objects.proxy_map[self].getPos())
        
    def left(self):
        objects.proxy_map[self].left()
        
    def right(self):
        objects.proxy_map[self].right()
        
    def stop(self):
        objects.proxy_map[self].stop()

# the internal Paddle object
class _Paddle:
    proxy_type = Paddle

    def __init__(self, pos):
        self.pos = pos
        self.dim = Vec2d(40, 10)

        # not walking yet
        self.dir = 0

    def destroy(self):
        pass

    def step(self, elapsed):
        # ds = v dt
        self.pos += Vec2d(move_speed * self.dir * elapsed, 0)

    def draw(self):
        # we're a little red rectangle
        rect = pygame.Rect(self.pos.x, self.pos.y, self.dim.x, self.dim.y)
        pygame.draw.rect(shared.canvas, (255, 0, 0), rect)

    def getPos(self):
        return self.pos
        
    def left(self):
        self.dir = -1
        
    def right(self):
        self.dir = +1
        
    def stop(self):
        self.dir = 0
