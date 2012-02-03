# ------------------------------------------------------------------
# levelname/__init__.py
# 
# A level!
# ------------------------------------------------------------------

import pygame

import shared
import objects
from vec2d import Vec2d
from level import Level

help_text = """
# 
# This is a template level.
# 
"""

# the main level class
class Main(Level):
    # called in the beginning of the game
    def __init__(self):
        Level.__init__(self)

    # called when the level starts
    def start(self):
        pass

    # called each step during the level
    def step(self, elapsed):
        pass

    # called on pygame events
    def event(self, event):
        pass

    # called when the level ends
    def stop(self):
        objects.destroy_all()
        pass

