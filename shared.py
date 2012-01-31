# ------------------------------------------------------------------
# shared.py
# 
# Shared data needed by most files
# ------------------------------------------------------------------

import time
import vec2d

# Stuff visible to user code
userspace = {}

userspace['__builtins__'] = None
userspace['Vec2d'] = vec2d.Vec2d
userspace['wait'] = time.sleep
