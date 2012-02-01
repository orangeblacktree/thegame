# run this in-game

def move_to_x(x):
    # keep moving paddle to (paddle.y, x) until ball gets low
    while ball.getPos().y < window_dim.y - 40:
        if paddle.getPos().x + 20 > x:
            paddle.move('left')
        else:
            paddle.move('right')
        wait(0.1)

def collision_x(pos, vel):
    # x coordinate of collision point at bottom
    return pos.x + vel.x * ((window_dim.y - pos.y) / vel.y)

def reflect_at_x(pos, vel, intx):
    inty = ballpos1.y + abs(ballvel.y * ((intx - ballpos1.x) / ballvel.x))
    if (inty > window_dim.y):
        # no reflection, pass data forward
        move_to_x(collision_x(pos, vel))
    else:
        # reflection, pass reflected data
        move_to_x(collision_x(Vec2d(intx, inty), Vec2d(-vel.x, vel.y)))
            
while True:
    # weird stuff when ball near walls (data samples are not along straight path)
    posref = ball.getPos() # reference to actual ball position, not copy
    while posref.y < 40 or window_dim.y - posref.y < 40 or posref.x < 40 or window_dim.x - posref.x < 40:
        wait(0.2)
        
    # get some sample data    
    delta_t = 0.2
    ballpos0 = Vec2d(posref)
    wait(delta_t)
    ballpos1 = Vec2d(posref)
    ballvel = (ballpos1 - ballpos0) / delta_t
    
    # work only while going down
    if ballvel.y > 0:
        if ballvel.x < 0:
            # going left: check reflection at x = 0
            reflect_at_x(ballpos1, ballvel, 0)
        else:
            # going right: check reflection at x = window_dim.x
            reflect_at_x(ballpos1, ballvel, window_dim.x)
        
    # can't think too fast...
    wait(0.2)
