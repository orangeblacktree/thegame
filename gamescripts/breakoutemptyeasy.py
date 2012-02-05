while True:
    if paddle.get_position().x > ball.get_position().x:
        paddle.set_motion('left')
    else:
        paddle.set_motion('right')
    wait(0.05)