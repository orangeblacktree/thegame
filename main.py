# ------------------------------------------------------------------
# main.py
# 
# Initialise stuff, handle events, main loop
# ------------------------------------------------------------------

import pygame
import pygtk
import gtk
import threading
import os

from vec2d import Vec2d
import shared
import objects
import player

# some settings
window_dimensions = (640, 480) #(width, height)
background_color = (0,0,0) #black
step_time = 40.0

def start():
    # the namespace that user code runs in
    shared.userspace = {}

    # set WM_CLASS under X
    os.environ['SDL_VIDEO_X11_WMCLASS'] = "thegame"
    gtk.gdk.set_program_class("thegame")

    # initialise gtk
    gtk.threads_init()
    shared.gtkwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
    shared.gtkwin.show()

    # initialise pygame
    pygame.init()
    global clock
    clock = pygame.time.Clock()
    shared.canvas = pygame.display.set_mode(window_dimensions)

    # set window titles
    pygame.display.set_caption("thegame - world", "thegame")
    shared.gtkwin.set_title("thegame - code editor")

    # create player
    p = objects.create(player._Player, Vec2d(window_dimensions) / 2)

    # test player proxy
    shared.userspace['player'] = p.proxy
    exec("player.test()", shared.userspace, shared.userspace)

def handleEvents():
    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            map(lambda o: o.keydown(event), objects.world)
        if event.type == pygame.KEYUP:
            map(lambda o: o.keyup(event), objects.world)

    return True

def loop():
    # run gtk main loop in separate thread
    class GtkLoop(threading.Thread):
        def run(self):
            gtk.main()
    gtkLoop = GtkLoop()
    gtkLoop.start()

    # game loop
    while True:
        # events
        if not handleEvents():
            break

        # action!
        map(lambda o: o.step(1 / step_time), objects.world)

        # draw pretty things
        shared.canvas.fill(background_color)
        map(lambda o: o.draw(), objects.world)
        pygame.display.update()

        # not so fast
        clock.tick(step_time)

def end():
    objects.destroy_all()

    gtk.threads_enter()
    gtk.main_quit()
    gtk.threads_leave()

    pygame.quit()

# play the game!
start()
loop()
end()

