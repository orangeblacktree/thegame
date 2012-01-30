# ------------------------------------------------------------------
# player.py
# 
# Player!
# ------------------------------------------------------------------

import pygame

import shared
from vec2d import Vec2d

# some settings
move_speed = 120

# the internal Player object
class _Player:
    def __init__(self, pos):
        self.pos = pos
        self.vel = Vec2d(0, 0)

        # not walking yet
        self.walking = False

    def step(self, elapsed):
        # move!
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
        # rectangle
        rect = pygame.Rect(self.pos.x, self.pos.y, 10, 10)
        pygame.draw.rect(shared.canvas, (255, 0, 0), rect)

    def keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.walk(1, Vec2d(-move_speed, 0))
        if event.key == pygame.K_RIGHT:
            self.walk(1, Vec2d(move_speed, 0))
        if event.key == pygame.K_UP:
            self.walk(1, Vec2d(0, -move_speed))
        if event.key == pygame.K_DOWN:
            self.walk(1, Vec2d(0, move_speed))

    def keyup(self, event):
        pass

    def walk(self, time, vel):
        if self.walking:
            return

        self.walking = True
        self.walk_timer = time
        self.vel = vel
