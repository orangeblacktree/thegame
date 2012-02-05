def move_to(x, t):
    print t, 
    t_m = abs(x - paddle.get_position().x) / paddle_speed + 0.7
    delta_t = t - t_m
    print delta_t
    if delta_t > 0:
        n = delta_t // 1
        r = delta_t - n
        for i in range(int(n * 4)):
            paddle.set_motion('right')
            wait(0.125)
            paddle.set_motion('left')
            wait(0.125)
        wait(r)
    
    if paddle.get_position().x < x:
        paddle.set_motion('right')
        while paddle.get_position().x < x and ball.get_position().y < paddle.get_position().y - 48:
            wait(0.1)
    else:
        paddle.set_motion('left')
        while paddle.get_position().x > x and ball.get_position().y < paddle.get_position().y - 48:
            wait(0.1)
    paddle.set_motion('stop')
    while ball.get_position().y < paddle.get_position().y - 60:
        wait(0.1)
    wait(0.5)

def hor_intersect(pos, vel, pady, t0):
    t = (pady - pos.y) / vel.y
    intx = pos.x + vel.x * t
    
    move_to(intx, t0 + t)

def vert_intersect(pos, vel, intx, pady, t0):
    t = (intx - pos.x) / vel.x
    inty = pos.y + vel.y * t
    
    if inty < pady:
        hor_intersect(Vec2d(intx, inty), Vec2d(-vel.x, vel.y), pady, t0 + t)
    else:
        hor_intersect(pos, vel, pady, t0)
        
def top_intersect(pos, vel, t0):
    pady = paddle.get_position().y
    
    if vel.x > 0:
        vert_intersect(pos, vel, right_wall, pady, t0)
    else:
        vert_intersect(pos, vel, left_wall, pady, t0)
        
def hor_upintersect(pos, vel, t0):
    t = (top_wall - pos.y) / vel.y
    intx = pos.x + vel.x * t
    top_intersect(Vec2d(intx, top_wall), Vec2d(vel.x, -vel.y), t0 + t)
        
def vert_upintersect(pos, vel, intx, t0):
    t = (intx - pos.x) / vel.x
    inty = pos.y + vel.y * t
    
    if inty > top_wall:
        hor_upintersect(Vec2d(intx, inty), Vec2d(-vel.x, vel.y), t0 + t)
    else:
        hor_upintersect(pos, vel, t0)

while True:
    pos = ball.get_position()
    
    if pos.y < top_wall + 30 or pos.y > paddle.get_position().y - 30: 
        wait(0.2)
        continue
        
    vel = ball.get_velocity()
    
    if vel.y > 0:    
        top_intersect(pos, vel, 0)
    elif vel.x > 0:
        vert_upintersect(pos, vel, right_wall, 0)
    elif vel.x < 0:
        vert_upintersect(pos, vel, left_wall, 0)
        
    wait(0.2)