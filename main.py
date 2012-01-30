# ------------------------------------------------------------------
# main.py
# 
# Initialise stuff, handle events, main loop
# ------------------------------------------------------------------

import pygame

import shared
from vec2d import Vec2d
import player

# some settings
window_dimensions = (640, 480) #(width, height)
background_color = (0,0,0) #black
step_time = 40.0

# initialise pygame
pygame.init()
clock = pygame.time.Clock()

# initialise window
shared.canvas = pygame.display.set_mode(window_dimensions)

# test player
player = player._Player(Vec2d(window_dimensions) / 2)
shared.objects = [player]

# main loop
running = True
while running:
    # events
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
            map(lambda o: o.keydown(event), shared.objects)
        if event.type == pygame.KEYUP:
            map(lambda o: o.keyup(event), shared.objects)

    # still running?
    if not running:
        break

    # action!
    map(lambda o: o.step(1 / step_time), shared.objects)

    # background
    shared.canvas.fill(background_color)

    # draw stuff
    map(lambda o: o.draw(), shared.objects)
    pygame.display.update()

    # not so fast!
    clock.tick(step_time)

# finish
pygame.quit()
