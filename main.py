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
import sys
import traceback

from vec2d import Vec2d
import shared
import userspace
import gui
import objects
import player

background_color = (0,0,0) #black
frame_rate = 40.0

shared.stop_game = False

def init():
    # set WM_CLASS under X
    os.environ['SDL_VIDEO_X11_WMCLASS'] = "thegame"
    gtk.gdk.set_program_class("thegame")

    # initialise gtk
    gtk.threads_init()
    shared.gtkwin = gtk.Window(gtk.WINDOW_TOPLEVEL)
    shared.gui = gui.Gui()

    # window sizes/positions
    gtkscreen = shared.gtkwin.get_screen()
    dim = Vec2d(gtkscreen.get_width(), 
            gtkscreen.get_height())

    pygame_pos = dim * 0.01
    pygame_dim = dim * (0.65, 0.75)
    gtk_pos = dim * (0.55, 0.4)
    gtk_dim = dim * (0.44, 0.55)

    shared.gtkwin.move(int(gtk_pos.x), int(gtk_pos.y))
    shared.gtkwin.resize(int(gtk_dim.x), int(gtk_dim.y))

    shared.dim = pygame_dim
    userspace.space['window_dim'] = pygame_dim
    
    # initialise pygame
    pygame.init()
    global clock
    clock = pygame.time.Clock()
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pygame_pos.x, pygame_pos.y)
    shared.canvas = pygame.display.set_mode((int(pygame_dim.x), 
        int(pygame_dim.y)))

    # set window titles
    shared.gtkwin.show()
    shared.gtkwin.set_title("thegame - code editor")
    pygame.display.set_caption("thegame - world", "thegame")

    # set keybindings
    userspace.resetKeybindings()

    # create player
    # p = objects.create(player._Player, Vec2d(pygame_dim) / 2)
    # userspace.space['player'] = p.proxy
    
    # start breakout level
    from breakout import Breakout
    b = Breakout()

def handleEvents():
    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            userspace.doKey(event.key)

    return True

def loop():
    # run gtk main loop in separate thread
    class GtkLoop(threading.Thread):
        def run(self):
            gtk.main()
    global gtk_thread
    gtk_thread = GtkLoop()
    gtk_thread.start()

    # game loop
    while not shared.stop_game:
        # events
        if not handleEvents():
            break

        # action!
        # TODO: fix elapsed time handling!
        elapsed = 1 / frame_rate
        map(lambda o: o.step(elapsed), objects.world)
        shared.gui.step(elapsed)

        # draw pretty things
        shared.canvas.fill(background_color)
        map(lambda o: o.draw(), objects.world)
        pygame.display.update()

        # not so fast
        clock.tick(frame_rate)

def end():
    objects.destroy_all()

    shared.gui.quit()

    gtk.threads_enter()
    gtk.main_quit()
    gtk.threads_leave()
    gtk_thread.join()

    pygame.quit()

# play the game!
if __name__ == '__main__':
    try:
        init()
        loop()
    except Exception, e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
    end()
