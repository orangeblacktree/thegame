# ------------------------------------------------------------------
# userspace.py
# 
# Stuff visible to user code
# ------------------------------------------------------------------

import time
import vec2d
import pygame

space = {}

space['Vec2d'] = vec2d.Vec2d

# sleep in blocks of 'wait_block' to allow killing of thread
wait_block = 1
def wait(t):
    loops = t // wait_block
    extra = t - float(loops * wait_block)
    print loops, extra

    while loops > 0:
        loops -= 1
        time.sleep(wait_block)
    if (extra):
        time.sleep(extra)
space['wait'] = wait

