# ------------------------------------------------------------------
# objects.py
# 
# The game objects such as Player etc.
# ------------------------------------------------------------------

world = []
proxy_map = {}
destroy_requests = []

def create(cons, *args):
    obj = cons(*args)
    world.append(obj)

    # if type uses proxy_map, create one
    if hasattr(cons, 'proxy_type'):
        proxy = cons.proxy_type()
        obj.proxy = proxy
        proxy_map[proxy] = obj

    return obj

def handleRequests():
    map(destroy, destroy_requests)
    
def requestDestroy(obj):
    destroy_requests.append(obj)
    
def destroy(obj):
    if hasattr(obj, 'proxy'):
        del proxy_map[obj.proxy]
    obj.destroy()
    world.remove(obj)

def destroy_all():
    map(destroy, world)

