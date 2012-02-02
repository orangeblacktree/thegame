# ------------------------------------------------------------------
# text.py
# 
# A static text object
# ------------------------------------------------------------------

import pygame
import shared
import objects
from vec2d import Vec2d

class Text:
    def __init__(self, text = "", position = Vec2d(0, 0), size = 48, font_type = None, color = (255, 255, 255)):
        self.text = text
        self.pos = Vec2d(position)
        self.size = size
        self.font_type = font_type
        self.color = color

        self.update_font()

    def update_font(self):
        self.font = pygame.font.Font(self.font_type, self.size)
        self.update_image()
    def update_image(self):
        self.image = self.font.render(self.text, 1, self.color)

    def set_text(text):
        self.text = text
        self.update_image()
    def set_position(pos):
        self.pos = Vec2d(pos)
    def set_size(size):
        self.size = size
        self.update_font()
    def set_font_type(font_type):
        self.font_type = font_type
        self.update_font()
    def set_color(color):
        self.color = color
        self.update_image()

    def set_properties(self, text = None, position = None, size = None, font_type = None, color = None):
        update_font = False
        update_image = False

        if text is not None:
            self.set_text(text)
            update_image = True
        if position is not None:
            self.pos = Vec2d(position)
        if size is not None:
            self.size = size
            update_font = True
        if font_type is not None:
            self.font_type = font_type
            update_font = True
        if color is not None:
            self.color = color
            update_image = True

        if update_font:
            self.update_font()
        elif update_image: # update_font() updates image too
            self.update_image()

    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        shared.canvas.blit(self.image, self.pos)
        
    def select(self):
        pass
