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
move_speed = 120

# the user's interface to the Player
class Player:
    def test(self):
        objects.proxy_map[self].walk(3, Vec2d(-move_speed, 0))

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
                self.vel *= 1 - 2*elapsed
            if self.walk_timer <= 0:
                self.vel = Vec2d(0, 0)
                self.walking = False

    def draw(self):
        # we're a little red square
        rect = pygame.Rect(self.pos.x, self.pos.y, 10, 10)
        pygame.draw.rect(shared.canvas, (255, 0, 0), rect)

    def keydown(self, event):
        # temporary key mappings
        keymap = {
            pygame.K_LEFT : Vec2d(-move_speed, 0),
            pygame.K_RIGHT : Vec2d(move_speed, 0),
            pygame.K_UP : Vec2d(0, -move_speed),
            pygame.K_DOWN : Vec2d(0, move_speed),
        }
        vel = keymap.get(event.key)
        if vel:
            self.walk(1, vel)

    def keyup(self, event):
        pass

    def walk(self, time, vel):
        # start walking if not walking already
        if not self.walking:
            self.walking = True
            self.walk_timer = time
            self.vel = vel
