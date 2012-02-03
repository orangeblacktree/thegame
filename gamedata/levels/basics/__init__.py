# ------------------------------------------------------------------
# basics/__init__.py
# 
# Teaches basics
# ------------------------------------------------------------------

import os

import pygame

import shared
import objects
import userspace
from vec2d import Vec2d
from level import Level
import image

helps = { 
'move': """
# In thegame, you do things through code. We shall use Python, a popular
# programming language. This tab will give you instructions that help
# you through the game.
#
# Open a new tab (File Menu -> New Tab) and paste in the following code:
 
player.move('right')

# Now run the code (while on the new tab, Run Menu -> Run). You should see the
# red block move one step to the right.
""",

}

base_path = os.path.join('gamedata', 'levels', 'basics')

grid_path = os.path.join(base_path, 'grid.png')
player_path = os.path.join(base_path, 'player.png')

def in_bounds(vec):
    return vec.x > 32 and vec.x < shared.dim.x - 32 and vec.y > 32 and vec.y < shared.dim.y - 32

# the main level class
class Main(Level):
    # called in the beginning of the game
    def __init__(self):
        Level.__init__(self)
        self.name = "Basics 1"

    # called when the level starts
    def start(self):
        shared.gui.help_page.set_text(helps['move'])

        # make the background grid
        objects.create(image.Image, grid_path, (0, 0))

        # make the player
        objects.create(_Player, (176, 176))

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

# Player interface visible to user code
class Player:
    def move(self, dirstr):
        dirs = { 'left': Vec2d(-32, 0), 'right': Vec2d(32, 0),
                'up': Vec2d(0, -32), 'down': Vec2d(0, 32) }
        vec = dirs.get(dirstr)
        if vec:
            objects.proxy_map[self].move(vec)

# internal Player
class _Player:
    proxy_type = Player

    # object events

    def __init__(self, proxy, pos):
        self.pos = Vec2d(pos)
        self.sprite = pygame.image.load(player_path)

        userspace.space['player'] = proxy

    def destroy(self):
        del userspace.space['player']
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        # our origin is at 16, 16 relative to the image (on the center)
        shared.canvas.blit(self.sprite, self.pos - Vec2d(16, 16))


    # player functions 

    def move(self, vec):
        new = self.pos + vec
        if (in_bounds(new)):
            self.pos = new


