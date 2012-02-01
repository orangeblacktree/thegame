import pygame
import os
import shared
import objects
import userspace

from levelchoice import LevelChoice, _LevelChoice
from text import Text, _Text

class LevelChooser:
    def __init__(self):
        # set up/down keybindings
        userspace.space['keybindings'] = {
            "up" : "moveUp()",
            "down" : "moveDown()",
            "enter" : "selectLevel()"
        }
        levels = os.listdir("./levels/")
        t = objects.create(_Text)
        t.update(text="Choose your level", pos=(30, 10), size=64, color=(255,150,150))
        for i, name in enumerate(levels):
            objects.create(_LevelChoice, i, name)
