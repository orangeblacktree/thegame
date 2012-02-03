# ------------------------------------------------------------------
# basics/__init__.py
# 
# Teaches basics
# ------------------------------------------------------------------

import os

import pygame

import shared
import objects
import userspace
from vec2d import Vec2d
from level import Level
import image

helps = { 

'move': """
# In thegame, you do things through code. We shall use Python, a popular
# programming language. This tab will give you instructions that help
# you through the game.
#
# Open a new tab (File Menu -> New Tab) and paste in the following code:
 
player.move('right')

# Now run the code (while on the new tab, Run Menu -> Run). You should see the
# red block move one step to the right.
""",

'otherdirs': """
# Well done!
# 
# 'player' refers to the player object (the red block). 'move' is a function you
# called on the player, which made it move. You gave it a parameter that
# specified the direction to move in. 
#
# The other directions are '%s', '%s' and '%s'. Try them too.
""",

'loops': """
# Well done!
# 
# 'player' refers to the player object (the red block). 'move' is a function you
# called on the player, which made it move. You gave it a parameter that
# specified the direction to move in. 
#
# The other directions are '%s', '%s' and '%s'. Try them too.
""",

'output': """
# You can print text to the output console using the 'output' function. Try 
# running the code below:

output('Hello, world!')
""",

'variables': """
# Variables allow you to assign names to values. The below code assigns the value
# 5 to a variable called 'number' and prints it.

number = 5
output(number)

# Try creating your own variable and printing it.
""",

'lists': """
# We have seen numbers, strings (such as 'left' and 'right') and complex objects
# such as the player. An interesting type that is built into Python is the 'list'.
# A list is simply an ordered collection of elements. Each of these elements is
# yet another Python object.
#
# Here we create a list named 'l' and print it.

l = [1, 2, 3, 4] # a list of the numbers 1, 2, 3 and 4
output(l)

# Try printing your own list.
""",

'loops': """
# Good job!
#
# Loops run the same code multiple times. The 'for' loop can be used to iterate
# over items in a list. Each time it runs the code with a different element of
# the list. In the below example, "output(i)" is run repeatedly with different
# values for 'i'. The for statement above it says that these values for i must
# be picked from the list [1, 2, 3]. The code to be run inside a for loop must
# be indented.

for i in [1, 2, 3]:
    output(i)
output('done!')

# Let's get back to the game. Try running the following piece of code. The
# wait(s) function pauses execution for 's' seconds.

# do this three times
for i in range(3):
    # move in each direction
    for dir in ['left', 'up', 'right', 'down']:
        output('Going ' + dir + '!')

        player.move(dir)

        wait(1) # wait for 1 second so we don't move too fast

# If your code ever gets stuck in an infinite loop you can use cancel its 
# execution with Run Menu -> Cancel.
""",

'end': """
# Move the player to the yellow square to complete the level.
"""

}

base_path = os.path.join('gamedata', 'levels', 'basics')

grid_path = os.path.join(base_path, 'grid.png')
player_path = os.path.join(base_path, 'player.png')
endblock_path = os.path.join(base_path, 'end.png')

grid_step = 32

end_pos = Vec2d(0, 0) #updated later

def in_bounds(vec):
    return vec.x > grid_step and vec.x < shared.dim.x - grid_step and vec.y > grid_step and vec.y < shared.dim.y - grid_step

# help state info
inoutput = False
invariables = False
inlists = False
inloops = False
oldsize = 0
moved = False
otherdirs = []

def output(s):
    global inoutput
    global invariables
    global oldsize
    global inlists
    global inloops

    userspace.output(s)

    if inoutput:
        inoutput = False
        shared.gui.help_page.append_text(helps['variables'])
        oldsize = len(userspace.space)
        invariables = True
    elif invariables and len(userspace.space) > oldsize:
        invariables = False
        shared.gui.help_page.append_text(helps['lists'])
        inlists = True
    elif inlists and type(s) == list:
        inlists = False
        shared.gui.help_page.set_text(helps['loops'])
        inloops = True


# the main level class
class Main(Level):
    # called in the beginning of the game
    def __init__(self):
        Level.__init__(self)
        self.name = "Basics 1"
        self.data.completed = False
        self.won = False

    # called when the level starts
    def start(self):
        global inoutput
        inoutput = False
        global invariables
        invariables = False
        global inlists
        inlists = False
        global inloops
        inloops = False
        global moved
        moved = False
        global otherdirs
        otherdirs = []

        end_pos = shared.dim + Vec2d(200, 200)

        shared.gui.help_page.set_text(helps['move'])

        # use our own output function
        userspace.space['output'] = output

        # make the background grid
        objects.create(image.Image, grid_path, (0, 0))

        # make the player
        player = objects.create(_Player, grid_step * Vec2d(5.5, 5.5))
        userspace.space['player'] = player.proxy

    # called each step during the level
    def step(self, elapsed):
        pass

    # called on pygame events
    def event(self, event):
        pass

    # called when the level ends
    def stop(self):
        objects.destroy_all()
        userspace.space['output'] = userspace.output #restore output()

        if not self.won:
            shared.gui.help_page.clear_text()

# Player interface visible to user code
class Player:
    def move(self, dirstr):
        global moved
        global otherdirs
        global inloops

        player = objects.proxy_map[self]
        dirs = { 'left': Vec2d(-grid_step, 0), 'right': Vec2d(grid_step, 0),
                'up': Vec2d(0, -grid_step), 'down': Vec2d(0, grid_step) }
        vec = dirs.get(dirstr)
        if vec:
            if not moved:
                otherdirs = list(dirs.iterkeys())
                otherdirs.remove(dirstr)
                shared.gui.help_page.append_text(
                        helps['otherdirs'] % tuple(otherdirs))
                moved = True
            elif dirstr in otherdirs:
                shared.gui.help_page.append_text(helps['output'])
                global inoutput
                inoutput = True
                otherdirs = []
            elif inloops:
                shared.gui.help_page.set_text(helps['end'])
                global end_pos
                end_pos = shared.dim - grid_step * Vec2d(6, 6)
                objects.create(image.Image, endblock_path, end_pos)
                inloops = False

            player.move(vec)

            # check if we won
            pos = player.pos
            if (pos.x > end_pos.x and pos.x < end_pos.x + grid_step 
                    and pos.y > end_pos.y and pos.y < end_pos.y + grid_step):
                shared.levelmgr.get_current_level().data.completed = True
                shared.levelmgr.get_current_level().won = True
                shared.levelmgr.request_next_level()
                shared.gui.help_page.set_text("# Well done! You completed 'Basics 1'")

        else:
            userspace.output("Error: '%s' is not a valid direction!" % (dirstr))

# internal Player
class _Player:
    proxy_type = Player
    
    # object events
    def __init__(self, proxy, pos):
        self.pos = Vec2d(pos)
        self.sprite = pygame.image.load(player_path)

    def destroy(self):
        del userspace.space['player']
        
    def step(self, elapsed):
        pass
        
    def draw(self):
        # our origin is at 16, 16 relative to the image (on the center)
        shared.canvas.blit(self.sprite, self.pos - grid_step * Vec2d(0.5, 0.5))


    # player functions 

    def move(self, vec):
        new = self.pos + vec
        if (in_bounds(new)):
            self.pos = new


