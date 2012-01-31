# ------------------------------------------------------------------
# userspace.py
# 
# Things related to user code execution
# ------------------------------------------------------------------

import time
import vec2d
import pygame

# a 'wait()' function for user code - sleep in blocks to allow
# cancelling
wait_block = 1
def wait(t):
    loops = t // wait_block
    extra = t - float(loops * wait_block)

    while loops > 0:
        loops -= 1
        time.sleep(wait_block)
    if (extra):
        time.sleep(extra)

# the space visible to user code
space = dict(
        Vec2d = vec2d.Vec2d,
        wait = wait
        )

# run code in user space
def run(code):
    exec(code, space, space)

# reset keybindings to defaults
def resetKeybindings():
    space['keybindings'] = {
        pygame.K_LEFT: "player.walk('left')",
        pygame.K_RIGHT: "player.walk('right')",
        pygame.K_UP: "player.walk('up')",
        pygame.K_DOWN: "player.walk('down')",
    }

# run action associated with a keybinding
def doKey(key):
    if 'keybindings' not in space or type(space['keybindings']) is not dict:
        resetKeybindings()
    if key in space['keybindings']:
        code = space['keybindings'][key]
        run(code)
