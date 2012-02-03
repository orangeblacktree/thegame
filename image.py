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
    # 'convert' is whether to convert to display format for performance

    def __init__(self, filename = None, position = Vec2d(0, 0), convert = True):
        self.image = None
        self.pos = position
        self.convert = convert

        self.set_image_file(filename)

    def set_image_file(self, filename):
        if filename:
            self.image = pygame.image.load(filename)
            if self.convert:
                self.image = pygame.Surface.convert(self.image)
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

