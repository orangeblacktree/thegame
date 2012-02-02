def intersects(r1, r2):
    return (r1.x <= r2.x + r2.width and
       r1.x + r1.width >= r2.x and
       r1.y <= r2.y + r2.height and
       r1.y + r1.height >= r2.y and
       r2.x <= r1.x + r1.width and
       r2.x + r2.width >= r1.x and
       r2.y <= r1.y + r1.height and
       r2.y + r2.height >= r1.y)
       
if __name__ == '__main__':
    import pygame

    r1 = pygame.Rect(0,0,10,10)
    r2 = pygame.Rect(5,5,15,15)
    r3 = pygame.Rect(11,11,14,14)
    assert intersects(r1,r2)
    assert intersects(r2,r3)
    assert not intersects(r1,r3)
