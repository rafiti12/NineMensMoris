from constants import *


class Tile:
    owner = Owner.NONE

    def __init__(self, POSITION, INDEX):
        self.POSITION = POSITION
        self.INDEX = INDEX

    def addMills(self, MILLS):
        self.MILLS = MILLS

    def addNeighbors(self, NEIGHBORS):
        self.NEIGHBORS = NEIGHBORS

    def checkForMill(self, tiles):
        for m in self.MILLS:
            if self.owner == tiles[m[0]].owner and self.owner == tiles[m[1]].owner:
                return True
        return False

    def checkForMove(self, index, tiles):
        for n in self.NEIGHBORS:
            if n == index:
                return True
        return False
