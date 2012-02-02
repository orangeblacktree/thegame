# ------------------------------------------------------------------
# text.py
# 
# A static text object
# ------------------------------------------------------------------

import pygame
import shared
import objects

class _Text:
    def __init__(self):
        self.text = ""
        self.pos = (0,0)
        self.size = 12
        self.fontType = None
        self.font = pygame.font.Font(self.fontType, self.size)
        self.color = (0,0,0)
        self.img = self.font.render(self.text, 1, self.color)

    def render(self):
        self.img = self.font.render(self.text, 1, self.color)

    def update(self, text=None, pos=None, size=None,  fontType=None, color=None):
        if text is not None:
            self.text = text
        if pos is not None:
            self.pos = pos
        if size is not None:
            self.size = size
        if fontType is not None:
            self.fontType = fontType
        self.font = pygame.font.Font(self.fontType, self.size)
        if color is not None:
            self.color = color

        self.render()

    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        shared.canvas.blit(self.img, self.pos)
        
    def select(self):
        pass
