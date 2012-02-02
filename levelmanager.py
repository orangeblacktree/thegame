# ------------------------------------------------------------------
# levelmanager.py
# 
# Manage reading list of levels and switching between them
# ------------------------------------------------------------------

import importlib
import pickle

import gamedata.levels
import gamedata.levels.levelselect

levels_list_filename = 'gamedata/levels/list'

class LevelManager:
    def __init__(self):
        self.levels = {}
        self.current_level = -1
        self.requested_level = -1

        # add level select menu
        self.levels[0] = gamedata.levels.levelselect.Main()

        # add the levels
        self.parse_level_list(levels_list_filename)

    # add each level from file at 'path'
    def parse_level_list(self, path):
        f = open(path, 'r')
        for line in f:
            if line[0] == '#':
                continue #skip comments

            words = line.split()

            ind = int(words.pop(0))

            nextind = 0
            if words[0].isdigit(): #might skip nextind, 0 by default
                nextind = int(words.pop(0))

            modulename = words.pop(0)

            deps = list(map(int, words))

            self.add_level(ind, nextind, modulename, deps)

    # add level in module 'modulename'
    def add_level(self, ind, nextind, modulename, deps):
        mod = importlib.import_module('gamedata.levels.' + modulename, gamedata.levels)

        level = mod.Main()
        level.ind = ind
        level.next_level = nextind
        level.deps = deps

        self.levels[ind] = level

    # start the game
    def start(self):
        if self.current_level < 0:
            self.goto_level(0)

    # stop the game
    def stop(self):
        if self.current_level >= 0:
            self.levels[self.current_level].stop()
        self.current_level = -1

    # jump to a given level if it's unlocked, else go to 0
    def goto_level(self, ind):
        if self.unlocked(self.levels[ind]):
            self.current_level = ind
        elif self.current_level != 0:
            self.current_level = 0
        else:
            return #target locked and we're already at 0
        if self.current_level >= 0:
            self.levels[self.current_level].stop()
        self.levels[self.current_level].start()
    def request_goto_level(self, ind):
        self.requested_level = ind

    # go to the next level
    def next_level(self):
        if self.current_level < 0:
            self.goto_level(0)
        else:
            nxt = self.levels[self.current_level].next_level
            self.goto_level(nxt)
    def request_next_level(self):
        if self.current_level < 0:
            self.request_goto_level(0)
        else:
            nxt = self.levels[self.current_level].next_level
            self.request_goto_level(nxt)

    # notify current level of step event
    def step(self, elapsed):
        if self.current_level >= 0:
            self.levels[self.current_level].step(elapsed)

    # notify current level of a pygame event
    def event(self, event):
        if self.current_level >= 0:
            self.levels[self.current_level].event(event)

    # handle level switch requests
    def handle_requests(self):
        if self.requested_level >= 0:
            self.goto_level(self.requested_level)
            self.requested_level = -1

    # whether a level is playable
    def unlocked(self, level):
        if level.ind == 0:
            return True # level select menu is always unlocked
        for depind in level.deps:
            dep = self.levels[depind]
            if not dep.data.completed:
                return False
        return True

    # save level data for all levels to file
    def save_level_data(self, f):
        all_data = {}
        for ind, level in self.levels.iteritems():
            all_data[ind] = level.data
        pickle.dump(all_data, f)

    # load level data from file
    def load_level_data(self, f):
        all_data = pickle.load(f)
        for ind, data in all_data.iteritems():
            self.levels[ind].data = data

