# ------------------------------------------------------------------
# breakoutempty/__init__.py
# 
# Breakout without the bricks.
# ------------------------------------------------------------------

import pygame
import os
import math

import shared
import userspace
import objects
import image
import util
from vec2d import Vec2d
from level import Level

# help page texts
helps = { 
'breakout': """
# 
# Try to get 7 consecutive hits.
# 
""",

}


# settings
grid_step = 32

paddle_speed = 220
paddle_width = grid_step * 3
paddle_height = grid_step
paddle_dim = Vec2d(paddle_width, paddle_height)

ball_speed = 300
ball_width = grid_step * 0.75
ball_height = grid_step * 0.75
ball_dim = Vec2d(ball_width, ball_height)


# resources
basics_base_path = os.path.join('gamedata', 'levels', 'basics')
base_path = os.path.join('gamedata', 'levels', 'breakoutempty')

grid_path = os.path.join(basics_base_path, 'grid.png')
paddle_path = os.path.join(base_path, 'paddle.png')
ball_path = os.path.join(base_path, 'ball.png')


# global data
move_space = None #will be updated to a Rect that objects can move in
hits = 0 #number of successive Paddle hits


# the main level class
class Main(Level):
    # called in the beginning of the game
    def __init__(self):
        Level.__init__(self)
        self.name = "Breakout Minus Bricks"

        # Rect that objects are allowed to move inside
        global move_space
        move_space = pygame.Rect(grid_step, grid_step, shared.dim.x - 2*grid_step, shared.dim.y - 2*grid_step)

    # called when the level starts
    def start(self):
        shared.gui.help_page.set_text(helps['breakout'])

        # make the background grid
        objects.create(image.Image, grid_path, (0, 0))

        # Paddle and Ball
        self.paddle = objects.create(_Paddle, (shared.dim.x / 2, shared.dim.y - grid_step * 2.5))

        ballvel = Vec2d(1, 1)
        ballvel.length = ball_speed
        self.ball = objects.create(_Ball, (shared.dim.x / 2, shared.dim.y / 2), ballvel)

        # reset hits
        global hits
        hits = 0

    # called each step during the level
    def step(self, elapsed):
        # check for collision
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.collide(self.paddle.rect)

        # win?
        if hits >= 7:
            shared.levelmgr.get_current_level().data.completed = True
            #shared.levelmgr.request_next_level()
            shared.gui.help_page.set_text("# Well done! You got seven consecutive hits!")

    # called on pygame events
    def event(self, event):
        pass

    # called when the level ends
    def stop(self):
        objects.destroy_all()


# Paddle interface visible to user code
class Paddle:
    def get_position(self):
        return Vec2d(objects.proxy_map[self].rect.center)
    def set_motion(self, arg):
        vels = { 'left': Vec2d(-paddle_speed, 0), 'right': Vec2d(paddle_speed, 0),
                'stop': Vec2d(0, 0) }
        vel = vels.get(arg)
        if vel:
            objects.proxy_map[self].vel = vel
        else:
            userspace.output("Error: '%s' is not a valid motion!" % (arg))
# internal Paddle
class _Paddle:
    proxy_type = Paddle

    # object events
    def __init__(self, proxy, pos):
        self.proxy = proxy
        userspace.space['paddle'] = proxy

        # given position is Paddle origin, which is center of sprite
        self.rect = pygame.Rect(0, 0, paddle_width, paddle_height)
        self.rect.center = pos

        self.vel = Vec2d(0, 0)

        self.sprite = pygame.image.load(paddle_path)

    def destroy(self):
        del userspace.space['paddle']
        
    def step(self, elapsed):
        self.rect = self.rect.move(self.vel * elapsed).clamp(move_space)
        
    def draw(self):
        shared.canvas.blit(self.sprite, self.rect)


# Ball interface visible to user code
class Ball:
    def get_position(self):
        return Vec2d(objects.proxy_map[self].rect.center)
    def get_velocity(self):
        return Vec2d(objects.proxy_map[self].vel)
# internal Ball
class _Ball:
    proxy_type = Ball

    # object events

    def __init__(self, proxy, pos, vel):
        self.proxy = proxy
        userspace.space['ball'] = proxy

        # given position is Ball origin, which is center of sprite
        self.rect = pygame.Rect(0, 0, ball_width, ball_height)
        self.rect.center = pos

        self.vel = Vec2d(vel)

        self.sprite = pygame.image.load(ball_path)

    def destroy(self):
        del userspace.space['ball']
        
    def step(self, elapsed):
        newrect = self.rect.move(self.vel * elapsed)
        self.rect = newrect.clamp(move_space)

        # wall collision
        normal = Vec2d(self.rect.center) - Vec2d(newrect.center)
        if normal:
            if normal.y != 0:
                normal.x = 0
            self.reflect(normal)

            if normal.y < 0: #bottom wall hit
                global hits
                hits = 0

    def draw(self):
        shared.canvas.blit(self.sprite, self.rect)


    # Ball functions 

    def reflect(self, normal):
        self.vel = util.reflect(self.vel, normal)

    def collide(self, otherrect):
        # take shallowest axis-aligned intersection
        normal = Vec2d(self.rect.clip(otherrect).size)
        if normal.x < normal.y:
            normal.x = math.copysign(normal.x, self.rect.centerx - otherrect.centerx)
            self.vel.x = math.copysign(self.vel.x, normal.x)
            normal.y = 0
        else:
            normal.y = math.copysign(normal.y, self.rect.centery - otherrect.centery)
            self.vel.y = math.copysign(self.vel.y, normal.y)
            normal.x = 0

            if normal.y < 0: #Paddle top hit
                global hits
                hits += 1

        # correct position
        self.rect.move(normal)

