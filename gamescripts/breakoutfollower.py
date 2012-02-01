# run this in-game
while True:
    if paddle.getPos().x > ball.getPos().x:
        paddle.move('left')
    else:
        paddle.move('right')
    wait(1)
