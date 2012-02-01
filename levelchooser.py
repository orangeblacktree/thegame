class LevelChooser:
    def __init__(self):
        # set up/down keybindings
        keybindings["up"] = "moveUp()"
        keybindings["down"] = "moveDown()"
        keybindings["enter"] = "selectLevel()"
        
        levels = os.listdir("./levels/")
        for i, name in enumerate(levels):
            objects.create(_LevelChoice, i, name)
    