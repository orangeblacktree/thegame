# ------------------------------------------------------------------
# userspace.py
# 
# Things related to user code execution
# ------------------------------------------------------------------

import time
import vec2d
import pygame
import keymap

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

def myprint(s):
    print s+"X"
        
# the space visible to user code
space = dict(
        Vec2d = vec2d.Vec2d,
        wait = wait,
        )

# run code in user space
def run(code):
    exec(code, space, space)

# reset keybindings to defaults
def reset_keybindings():
    space['keybindings'] = {
        'left': "player.walk('left')",
        'right': "player.walk('right')",
        'up': "player.walk('up')",
        'down': "player.walk('down')",
    }
    space['keybindings'] = {
        pygame.K_LEFT: "paddle.move('left')",
        pygame.K_RIGHT: "paddle.move('right')",
    }
    space['keybindings'] = {
        pygame.K_LEFT: "paddle.move('left')",
        pygame.K_RIGHT: "paddle.move('right')",
    }

# run action associated with a keybinding
def do_key(keycode):
    if 'keybindings' not in space or type(space['keybindings']) is not dict:
        resetKeybindings()

    code = space['keybindings'].get(keymap.key_to_str[keycode])
    if code:
        run(code)
