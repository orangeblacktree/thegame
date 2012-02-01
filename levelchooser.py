import pygame
import os
import shared
import objects
import userspace

from levelchoice import LevelChoice, _LevelChoice

class LevelChooser:
    def __init__(self):
        # set up/down keybindings
        userspace.space['keybindings'] = {
            "up" : "moveUp()",
            "down" : "moveDown()",
            "enter" : "selectLevel()"
        }
        levels = os.listdir("./levels/")
        for i, name in enumerate(levels):
            objects.create(_LevelChoice, i, name)
