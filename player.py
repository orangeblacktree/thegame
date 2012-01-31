# ------------------------------------------------------------------
# player.py
# 
# Player!
# ------------------------------------------------------------------

import pygame

import shared
import objects
from vec2d import Vec2d

# some settings
move_speed = 50

# the user's interface to the Player
class Player:
    def walk(self, dir):
        vel = {
            "left" : Vec2d(-move_speed, 0),
            "right" : Vec2d(move_speed, 0),
            "up" : Vec2d(0, -move_speed),
            "down" : Vec2d(0, move_speed),
        }[dir]
        objects.proxy_map[self].walk(1, vel)

# the internal Player object
class _Player:
    proxy_type = Player

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
            if self.walk_timer <= 1:
                self.vel *= 1 - elapsed + elapsed**2/2
            if self.walk_timer <= 0:
                self.vel = Vec2d(0, 0)
                self.walking = False

    def draw(self):
        # we're a little red square
        rect = pygame.Rect(self.pos.x, self.pos.y, 10, 10)
        pygame.draw.rect(shared.canvas, (255, 0, 0), rect)

    def walk(self, time, vel):
        # start walking if not walking already
        if not self.walking:
            self.walking = True
            self.walk_timer = time
            self.vel = vel
