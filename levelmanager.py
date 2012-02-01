# ------------------------------------------------------------------
# levelmanager.py
# 
# Manage reading list of levels and switching between them
# ------------------------------------------------------------------

class LevelManager:
    def __init__(self):
        self.levels = []
        self.current_level = -1

        self.parse_level_list("levels/list")

    def parse_level_list(self, path):
        f = open(path, 'r')
        for line in f:
            if line[0] == '#':
                continue

            words = line.split()

            ind = int(words.pop(0))

            nextind = 0
            if words[0].isdigit():
                nextind = int(words.pop(0))

            modulename = words.pop(0)

            deps = list(map(int, words))

            print ind, nextind, modulename, deps

    def add_level(self, ind, nextind, modulename, deps):
        pass

    # start the game
    def start(self):
        if self.current_level <= -1:
            self.goto_level(0)
        pass

    # stop the game
    def stop(self):
        if self.current_level >= 0:
            self.levels[self.current_level].stop()
        self.current_level = -1

    # jump to a given level
    def goto_level(self, ind):
        if self.current_level >= 0:
            self.levels[self.current_level].stop()
        self.current_level = ind
        self.levels[self.current_level].start()

    # go to the next level
    def next_level(self):
        if current_level < 0:
            self.start()
        else:
            nxt = self.levels[self.current_level].next_level
            self.goto_level(nxt)

    # notify current level of step event
    def step(self, elapsed):
        if self.current_level >= 0:
            self.levels[self.current_level].step(self, elapsed)
