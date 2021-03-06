# Tetris
"""The game of tetris!
Version 1: CLI Block Selection and Dropping"""

# Imports
import time
import sys
import pygame
import pprint
import random
from termcolor import colored

# Data
width = 10
height = 20

# Classes

class TetrominoBag():
    """Tetris Worlds uses a 2 (14 blocks) bag system. This class replicates that."""
    def __init__(self):
        """Attributes for class."""
        self.bag = {}
        self.TetrominoTypeList = ["I", "J", "L", "O", "S", "T", "Z"]

    def MakeDoubleBag(self):
        """Makes a bag of 2 of each tetromino type."""
        for i in self.TetrominoTypeList:
            self.bag.update({i : 2})

    def Choose(self):
        """Returns a choice from one of the blocks in the bag, and removes that block from the bag."""
        lst = [x for x in self.bag.keys()]
        choice = random.choices(lst, k=1)[0]
        self.bag.update({choice : self.bag.get(choice) - 1})
        return(choice)

class Grid():
    """
    Represents the tetris grids and the blocks on it.
    """
    def __init__(self, width, height, bag):
        """
        Attributes for class
        """
        self.matrix = [[0 for z in range(width)] for i in range(height)]
        """0 means block is empty. 1 means the block is settled. 2 means the block is dropping."""
        self.colorMatrix = [[(0,0,0) for z in range(width)] for i in range(height)]
        self.width = width
        self.height = height
        self.coords = ""
        self.bag = bag

    def NewBlock(self):
        """
        Creates a new block and returns the starting coordinates for that block.
        """
        for i in self.matrix:
            if 2 in i:
                return()
        blockType = self.bag.Choose()
        subtractor = {"I" : 4, "J" : 3, "L" : 3, "O" : 2, "S" : 3, "T" : 3, "Z": 3}
        x = random.randint(0, self.width - subtractor.get(blockType))
        coords = []
        if blockType == "I":
            coords = [(x + i, 0) for i in range(4)]
        if blockType == "J":
            coords = [(x + i, 0) for i in range(3)]
            coords.append((x, 1))
        if blockType == "L":
            coords = [(x + i, 0) for i in range(3)]
            coords.append((x + 2, 1))
        if blockType == "O":
            coords = [(x, 0), (x + 1, 0), (x, 1), (x + 1, 1)]
        if blockType == "Z":
            coords = [(x, 0), (x + 1, 0), (x + 1, 1), (x + 2, 1)]
        if blockType == "S":
            coords = [(x + 1, 0), (x + 2, 0), (x, 1), (x + 1, 1)]
        if blockType == "T":
            coords = [(x, 0), (x + 1, 0), (x + 2, 0), (x + 1, 1)]
        self.coords = coords
        return(coords)

    def BlockToMatrix(self):
        """Updates the matrix with the block."""
        for h in range(height):
            for w in range(width):
                if self.matrix[h][w] == 2:
                    self.matrix[h][w] = 0
        for i in self.coords:
            self.matrix[i[1]][i[0]] = 2

    def BlockNaturalDrop(self):
        """Block dropping due to gravity."""
        # Checks for collision
        for i in self.coords:
            if i[1] == self.height - 1:
                for i in self.coords:
                    self.matrix[i[1]][i[0]] = 1
                return()      
            if self.matrix[i[1] + 1][i[0]] == 1:
                for i in self.coords:
                    self.matrix[i[1]][i[0]] = 1
                return()
        self.coords = [(i[0], i[1] + 1) for i in self.coords]
        Grid.BlockToMatrix(self)

bag = TetrominoBag()
bag.MakeDoubleBag()
grid = Grid(width, height, bag)


while True:
    grid.NewBlock()
    grid.BlockToMatrix()
    grid.BlockNaturalDrop()
    #pprint.pprint(grid.matrix)
    for row in grid.matrix:
        for element in row:
            if element == 1:
                print(colored(element, "red"), end=" ")
            elif element == 2:
                print(colored(element, "blue"), end=" ")
            else:
                print(element, end=" ")
        print("")
    input()
# Functions
