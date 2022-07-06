from json import tool
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
    
    def countPossibleMills(self, tiles):
        possible_mills = 0
        for m in self.MILLS:
            if tiles[m[0]].owner == self.owner and tiles[m[1]].owner == Owner.NONE:
                possible_mills += 1
            elif tiles[m[0]].owner == Owner.NONE and tiles[m[1]].owner == self.owner:
                possible_mills += 1
    
        return possible_mills

    def checkForMove(self, index, tiles):
        for n in self.NEIGHBORS:
            if n == index:
                return True
        return False

    def canMove(self, tiles):
        directions = len(self.NEIGHBORS)
        for n in self.NEIGHBORS:
            if tiles[n].owner != Owner.NONE:
                directions -= 1
        if directions == 0:
            return False
        return True
