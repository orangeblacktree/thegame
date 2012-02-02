# ------------------------------------------------------------------
# breakout/__init__.py
# 
# Breakout Level!
# ------------------------------------------------------------------

import pygame
import random

import shared
import userspace
import objects
from vec2d import Vec2d

from level import Level

from brick import Brick, _Brick
from paddle import Paddle, _Paddle
from ball import Ball, _Ball

class Main(Level):
    def __init__(self):
        self.name = "Breakout"

    def start(self):
        random.seed()
        
        self.paddle = objects.create(_Paddle, Vec2d(int(shared.dim.x/2), int(shared.dim.y - 20)))
        self.ball = objects.create(_Ball, Vec2d(shared.dim) / 2)
        
        bricks = {}
        self._bricks = {}
        for row in xrange(0, 10):
            for col in xrange(0, int(shared.dim.x/40)):
                brick = objects.create(_Brick, Vec2d(40,20)*(col,row) + (5,5))
                bricks[(row, col)] = brick.proxy
                self._bricks[(row, col)] = brick
                
        userspace.space['bricks'] = bricks
        userspace.space['ball'] = self.ball.proxy
        userspace.space['paddle'] = self.paddle.proxy

    def stop(self):
        objects.destroy_all()
        
    def event(self, event):
        pass

    def step(self, elapsed):
        # collide
        ball = self.ball
        paddle = self.paddle
        
        for loc in self._bricks:
            brick = self._bricks[loc]
            if brick.broken:
                continue
                
            if ((ball.pos.y > brick.pos.y - ball.radius and ball.pos.y <  brick.pos.y + brick.dim.y + ball.radius) and
               (ball.pos.x > brick.pos.x - ball.radius and ball.pos.x <  brick.pos.x + brick.dim.x + ball.radius)):
                brick.broken = True
                if ball.pos.x > brick.pos.x+brick.dim.x or ball.pos.x < brick.pos.x:
                    ball.vel.y *= -1 + random.random()-.5
                if ball.pos.y > brick.pos.y+brick.dim.y or ball.pos.y < brick.pos.y:
                    ball.vel.x *= -1 + random.random()-.5
                    
            if ball.pos.y > paddle.pos.y - ball.radius and ball.pos.x > paddle.pos.x - ball.radius and ball.pos.x < paddle.pos.x + paddle.dim.x + ball.radius:
                ball.vel.y = -abs(ball.vel.y)
        
