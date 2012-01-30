# ------------------------------------------------------------------
# userspace.py
# 
# Stuff visible to user code
# ------------------------------------------------------------------

import time
import vec2d

space = {}

space['Vec2d'] = vec2d.Vec2d
space['wait'] = lambda t: time.sleep(t)

