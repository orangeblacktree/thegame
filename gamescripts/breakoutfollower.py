# run this in-game
while True:
    if paddle.getPos().x > ball.getPos().x:
        paddle.left()
    else:
        paddle.right()
    wait(.05)
