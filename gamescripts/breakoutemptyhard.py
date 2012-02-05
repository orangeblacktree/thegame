def move_to(x):
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

def hor_intersect(pos, vel, pady):
    t = (pady - pos.y) / vel.y
    intx = pos.x + vel.x * t
    
    move_to(intx)

def vert_intersect(pos, vel, intx, pady):
    t = (intx - pos.x) / vel.x
    inty = pos.y + vel.y * t
    
    if inty < pady:
        hor_intersect(Vec2d(intx, inty), Vec2d(-vel.x, vel.y), pady)
    else:
        hor_intersect(pos, vel, pady)
        
def top_intersect(pos, vel):
    pady = paddle.get_position().y
    
    if vel.x > 0:
        vert_intersect(pos, vel, right_wall, pady)
    else:
        vert_intersect(pos, vel, left_wall, pady)
        
def hor_upintersect(pos, vel):
    t = (top_wall - pos.y) / vel.y
    intx = pos.x + vel.x * t
    top_intersect(Vec2d(intx, top_wall), Vec2d(vel.x, -vel.y))
        
def vert_upintersect(pos, vel, intx):
    t = (intx - pos.x) / vel.x
    inty = pos.y + vel.y * t
    
    if inty > top_wall:
        hor_upintersect(Vec2d(intx, inty), Vec2d(-vel.x, vel.y))
    else:
        hor_upintersect(pos, vel)

while True:
    pos = ball.get_position()
    
    if pos.y < top_wall + 30 or pos.y > paddle.get_position().y - 30: 
        wait(0.2)
        continue
        
    vel = ball.get_velocity()
    
    if vel.y > 0:    
        top_intersect(pos, vel)
    elif vel.x > 0:
        vert_upintersect(pos, vel, right_wall)
    elif vel.x < 0:
        vert_upintersect(pos, vel, left_wall)
        
    wait(0.2)
        