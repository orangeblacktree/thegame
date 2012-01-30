# ------------------------------------------------------------------
# objects.py
# 
# The game objects such as Player etc.
# ------------------------------------------------------------------

world = []

def create(cons, *args):
    world.append(cons(*args))

def destroy(obj):
    obj.destroy()
    world.remove(obj)
