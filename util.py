# ------------------------------------------------------------------
# util.py
# 
# Some utilities
# ------------------------------------------------------------------

from vec2d import Vec2d

# get the reflected vector given an incident and an any-length
# normal vector
def reflect(incident, normal):
    return incident - 2 * incident.dot(normal) * normal / normal.get_length_sqrd()

