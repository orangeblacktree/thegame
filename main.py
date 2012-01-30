# ------------------------------------------------------------------
# main.py
# 
# Initialise stuff, handle events, main loop
# ------------------------------------------------------------------

import pygame
import pygtk
import gtk
import threading

import shared
from vec2d import Vec2d
import player

# some settings
window_dimensions = (640, 480) #(width, height)
background_color = (0,0,0) #black
step_time = 40.0

def start():
    shared.objects = []

    # initialise pygame
    pygame.init()
    global clock
    clock = pygame.time.Clock()
    shared.canvas = pygame.display.set_mode(window_dimensions)

    # initialise gtk
    gtk.threads_init()
    shared.gtkwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
    shared.gtkwin.show()

    # test player
    shared.objects.append(player._Player(Vec2d(window_dimensions) / 2))

def handleEvents():
    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            map(lambda o: o.keydown(event), shared.objects)
        if event.type == pygame.KEYUP:
            map(lambda o: o.keyup(event), shared.objects)

    return True

def loop():
    class GtkLoop(threading.Thread):
        def run(self):
            gtk.main()
    gtkLoop = GtkLoop()
    gtkLoop.start()

    while True:
        # events
        if not handleEvents():
            break

        # action!
        map(lambda o: o.step(1 / step_time), shared.objects)

        # draw pretty things
        shared.canvas.fill(background_color)
        map(lambda o: o.draw(), shared.objects)
        pygame.display.update()

        # not so fast
        clock.tick(step_time)

def end():
    gtk.threads_enter()
    gtk.main_quit()
    gtk.threads_leave()

    pygame.quit()

# play the game!
start()
loop()
end()

