# ------------------------------------------------------------------
# objects.py
# 
# The game objects such as Player etc.
# ------------------------------------------------------------------

world = []
proxy_map = {}
destroy_requests = []

def create(cons, *args):
    if hasattr(cons, 'proxy_type'):
        proxy = cons.proxy_type()
        obj = cons(proxy, *args)
        obj.proxy = proxy
        proxy_map[proxy] = obj
    else:
        obj = cons(*args)

    world.append(obj)

    return obj

def handle_requests():
    while destroy_requests:
        destroy(destroy_requests.pop())
    
def request_destroy(obj):
    destroy_requests.append(obj)
    
def destroy(obj):
    if hasattr(obj, 'proxy'):
        del proxy_map[obj.proxy]
    obj.destroy()
    world.remove(obj)

def destroy_all():
    global world
    for obj in world:
        if hasattr(obj, 'proxy'):
            del proxy_map[obj.proxy]
        obj.destroy()
    world = []

