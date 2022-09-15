class Evaluation:
    def __init__(self):
        self.move = None
        self.score = 0

def countTiles(_tiles, player):
    ret = 0
    for tile in _tiles:
        if tile.owner == player:
            ret += 1

    return ret