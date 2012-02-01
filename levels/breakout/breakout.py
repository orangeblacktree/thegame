# ------------------------------------------------------------------
# breakout.py
# 
# Player!
# ------------------------------------------------------------------

import pygame

import shared
import userspace
import objects
from vec2d import Vec2d

from brick import Brick, _Brick
from paddle import Paddle, _Paddle
from ball import Ball, _Ball

class Breakout:
    def __init__(self):
        paddle = objects.create(_Paddle, Vec2d(int(shared.dim.x/2), int(shared.dim.y - 20)))
        bricks = {}
        _bricks = {}
        for row in xrange(0, 10):
            for col in xrange(0, int(shared.dim.x/40)):
                brick = objects.create(_Brick, Vec2d(40,20)*(col,row) + (5,5))
                bricks[(row, col)] = brick.proxy
                _bricks[(row, col)] = brick
                
        ball = objects.create(_Ball, Vec2d(shared.dim) / 2, _bricks, paddle)
        userspace.space['bricks'] = bricks
        userspace.space['ball'] = ball.proxy
        userspace.space['paddle'] = paddle.proxy
