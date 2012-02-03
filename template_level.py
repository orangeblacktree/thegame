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

helps = { 
'template': """
# 
# This is a template level.
# 
""",

}

# the main level class
class Main(Level):
    # called in the beginning of the game
    def __init__(self):
        Level.__init__(self)
        self.name = "Template Level"

    # called when the level starts
    def start(self):
        shared.gui.help_page.set_text(helps['template'])

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

