# ------------------------------------------------------------------
# image.py
# 
# A static image object
# ------------------------------------------------------------------

import pygame
import shared
import objects
from vec2d import Vec2d

class Image:
    def __init__(self, filename = None, position = Vec2d(0, 0)):
        self.image = None
        self.pos = position
        self.set_image_file(filename)

    def set_image_file(self, filename):
        if filename:
            self.image = pygame.image.load(filename)
    def set_position(self, position):
        self.pos = position

    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        if self.image:
            shared.canvas.blit(self.image, self.pos)
        
    def select(self):
        pass

