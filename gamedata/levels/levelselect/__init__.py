# ------------------------------------------------------------------
# levelselect/__init__.py
# 
# Show a list of levels
# ------------------------------------------------------------------

import pygame
import os

import shared
import objects
import image
import text
from vec2d import Vec2d
from level import Level

logo_top = 5
title_topgap = 5
title_height = 0 #no title now

buttons_topgap = 20
buttons_left = 40
button_height = 40
button_gap = 10
buttons_bottom_gap = 5
buttons_top = 0 #will set later

done_color = (0, 170, 0) #finished level
new_color = (170, 170, 170) #not finished, not locked
locked_color = (90, 90, 90) #locked level

select_highlight = 1.5
selrect_color = (200, 200, 200)
selrect_gap = 10
selrect_thickness = 2

button_font = None 

class _LevelButton:
    def __init__(self, pos, level):
        self.pos = pos
        self.level = level
        self.enabled = shared.levelmgr.unlocked(level)
        self.selected = False

        # set color based on level deps/completion
        if not self.enabled:
            self.color = locked_color
        elif level.data.completed:
            self.color = done_color
        else:
            self.color = new_color

        # make the initial text image
        self.text = button_font.render(level.name, 1, self.color) 

    def destroy(self):
        pass
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        # draw the text image
        if not (self.too_high() or self.too_low()):
            shared.canvas.blit(self.text, self.pos)

        # draw border rectangle if selected
        if self.selected:
            w = self.text.get_width()
            h = self.text.get_height()
            rect = (self.pos.x - selrect_gap, self.pos.y - selrect_gap,
                    w + 2*selrect_gap, h + 2*selrect_gap)
            pygame.draw.rect(shared.canvas, selrect_color, rect, 
                    selrect_thickness)

    def select(self):
        self.selected = True
        # brighten the text image
        if self.enabled:
            newcol = map(lambda x: min(x * select_highlight, 255), self.color)
            self.text = button_font.render(self.level.name, 1, newcol)

    def deselect(self):
        self.selected = False
        # back to normal
        self.text = button_font.render(self.level.name, 1, self.color)

    def click(self):
        # let's go!
        if self.enabled:
            shared.levelmgr.request_goto_level(self.level.ind)

    # bounds checking
    def too_high(self):
        return self.pos.y < buttons_top
    def too_low(self):
        return self.pos.y + button_height >= shared.dim.y - buttons_bottom_gap
        
class Main(Level):
    def __init__(self):
        Level.__init__(self)
        self.ind = 0
        self.next_level = 0
        self.deps = []
        self.name = "Level Select Menu"
        self.selected = 0

        global button_font
        button_font = pygame.font.Font(None, button_height)

    def start(self):
        # make logo
        logo = objects.create(image.Image, os.path.join('gamedata', 'images', 'logo.png'))
        logo_left = (shared.dim.x - logo.image.get_width()) // 2
        logo.set_position(Vec2d(logo_left, logo_top))

        logo_height = logo.image.get_height()
        global buttons_top
        buttons_top = logo_top + logo_height + title_topgap + title_height

        # make title text
        #title = objects.create(text.Text, self.name, Vec2d(0, 0), 
        #        title_height, None, (200, 128, 25))
        #title_left = (shared.dim.x - title.image.get_width()) // 2
        #title.set_properties(position = Vec2d(title_left, 
        #        logo_top + logo_height + title_topgap))

        # make buttons
        levels = shared.levelmgr.levels
        self.buttons = []
        for i, ind in enumerate(sorted(levels.iterkeys())):
            if ind == self.ind:
                continue # skip self
            pos = Vec2d(buttons_left, buttons_top # gap for title
                    + (i - 1) * (button_height + button_gap)) # offset for i'th button
            self.buttons.append(objects.create(_LevelButton, pos, levels[ind]))

        # select last selected
        self.buttons[self.selected].select()
        self.check_scroll()

    def step(self, elapsed):
        pass

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.select_prev()
            elif event.key == pygame.K_DOWN:
                self.select_next()
            elif event.key == pygame.K_RETURN:
                self.click_selected()

    def check_scroll(self):
        selbutton = self.buttons[self.selected]
        if selbutton.too_high():
            self.move_buttons(Vec2d(0, button_height + button_gap))
        elif selbutton.too_low():
            self.move_buttons(Vec2d(0, -(button_height + button_gap)))
    def move_buttons(self, vec):
        for b in self.buttons:
            b.pos += vec

    def select_next(self):
        # if higher ok, deselect current and select it
        new = self.selected + 1
        if new < len(self.buttons) and self.buttons[new].enabled:
            self.buttons[self.selected].deselect()
            self.selected = new
            self.buttons[self.selected].select()
            self.check_scroll()
    def select_prev(self):
        # if lower ok, deselect current and select it
        new = self.selected - 1
        if new >= 0 and self.buttons[new].enabled:
            self.buttons[self.selected].deselect()
            self.selected = new
            self.buttons[self.selected].select()
            self.check_scroll()
    def click_selected(self):
        self.buttons[self.selected].click()

    def stop(self):
        objects.destroy_all()
        self.buttons = []

