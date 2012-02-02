# ------------------------------------------------------------------
# levelselect/__init__.py
# 
# Show a list of levels
# ------------------------------------------------------------------

import pygame

import shared
import objects
import text
from vec2d import Vec2d

buttons_top = 20
buttons_left = 20

button_height = 48
button_gap = 10

done_color = (0, 170, 0) #finished level
new_color = (170, 170, 170) #not finished, not locked
locked_color = (90, 90, 90) #locked level
highlight = 1.5

button_font = None 

class _LevelButton:
    def __init__(self, pos, level):
        self.pos = pos
        self.level = level
        self.enabled = shared.levelmgr.unlocked(level)

        # set color based on level deps/completion
        if not self.enabled:
            self.color = locked_color
        elif level.completed:
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
        shared.canvas.blit(self.text, self.pos)

    def select(self):
        # brighten the text image
        if self.enabled:
            newcol = map(lambda x: min(x * highlight, 255), self.color)
            self.text = button_font.render(self.level.name, 1, newcol)

    def deselect(self):
        # back to normal
        self.text = button_font.render(self.level.name, 1, self.color)

    def click(self):
        # let's go!
        if self.enabled:
            shared.levelmgr.request_goto_level(self.level.ind)
        
        
class Main:
    def __init__(self):
        self.ind = 0
        self.next_level = 0
        self.deps = []
        self.name = "Level Select Menu"

        global button_font
        button_font = pygame.font.Font(None, button_height)

    def start(self):
        # make title text
        title = text._Text()
        title.update(text = self.name, size = button_height, color = (200, 128, 25))
        text_left = buttons_left #(shared.dim - title.img.get_width()) // 2
        title.update(pos = (text_left, buttons_top))

        # make buttons
        levels = shared.levelmgr.levels
        self.buttons = []
        for i, ind in enumerate(sorted(levels.iterkeys())):
            if ind == self.ind:
                continue # skip self
            pos = Vec2d(buttons_left, buttons_top + i * (button_height + button_gap))
            self.buttons.append(objects.create(_LevelButton, pos, levels[ind]))

        # select first
        self.selected = 0
        self.buttons[self.selected].select()

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

    def select_next(self):
        # if higher ok, deselect current and select it
        new = self.selected + 1
        if new < len(self.buttons) and self.buttons[new].enabled:
            self.buttons[self.selected].deselect()
            self.selected = new
            self.buttons[self.selected].select()
    def select_prev(self):
        # if lower ok, deselect current and select it
        new = self.selected - 1
        if new >= 0 and self.buttons[new].enabled:
            self.buttons[self.selected].deselect()
            self.selected = new
            self.buttons[self.selected].select()
    def click_selected(self):
        self.buttons[self.selected].click()

    def stop(self):
        objects.destroy_all()
        self.buttons = []

