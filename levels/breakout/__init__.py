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

import collisions
from level import Level

from brick import Brick, _Brick
from paddle import Paddle, _Paddle
from ball import Ball, _Ball

class Main(Level):
    def __init__(self):
        Level.__init__(self)
        self.name = "Breakout"
        self.completed = True

    def start(self):
        random.seed()
        
        self.paddle = objects.create(_Paddle, Vec2d(int(shared.dim.x/2), int(shared.dim.y - 20)))
        self.ball = objects.create(_Ball, Vec2d(shared.dim) / 2)
        
        bricks = {}
        self._bricks = {}
        for row in xrange(0, 10):
            for col in xrange(0, int(shared.dim.x/40)):
                brick = objects.create(_Brick, pygame.Rect(40*col + 5, 20*row + 5, 38, 18))
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
                
            ballRect = pygame.Rect(ball.pos.x - ball.radius, ball.pos.y - ball.radius, 2*ball.radius, 2*ball.radius)
            if (collisions.intersects(ballRect, brick)):
                brick.broken = True

                if ball.pos.x > brick.x + brick.width or ball.pos.x < brick.x:
                    ball.vel.y *= -1 + random.random()-.5
                if ball.pos.y > brick.y + brick.height or ball.pos.y < brick.y:
                    ball.vel.x *= -1 + random.random()-.5
                    
            if ball.pos.y > paddle.pos.y - ball.radius and ball.pos.x > paddle.pos.x - ball.radius and ball.pos.x < paddle.pos.x + paddle.dim.x + ball.radius:
                ball.vel.y = -abs(ball.vel.y)
        
