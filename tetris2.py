# Tetris
"""The game of tetris!
Version 1: CLI Block Selection and Dropping
Version 2: Pygame Interface, Game Loss Detection, Block Movement"""

# Imports
import time
import sys
import pygame
import pprint
import random

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
        elif blockType == "J":
            coords = [(x + i, 0) for i in range(3)]
            coords.append((x, 1))
        elif blockType == "L":
            coords = [(x + i, 0) for i in range(3)]
            coords.append((x + 2, 1))
        elif blockType == "O":
            coords = [(x, 0), (x + 1, 0), (x, 1), (x + 1, 1)]
        elif blockType == "Z":
            coords = [(x, 0), (x + 1, 0), (x + 1, 1), (x + 2, 1)]
        elif blockType == "S":
            coords = [(x + 1, 0), (x + 2, 0), (x, 1), (x + 1, 1)]
        elif blockType == "T":
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
    
    def MoveBlock(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and width - 1 not in [i[0] for i in self.coords]:
            touchingSettled = False
            for i in self.coords:
                if touchingSettled == False and self.matrix[i[1]][i[0] + 1] == 1:
                    touchingSettled = True
            if touchingSettled == False:
                self.coords = [(i[0] + 1, i[1]) for i in self.coords]
        elif keys[pygame.K_LEFT] and 1 not in [i[0] for i in self.coords]:
            touchingSettled = False
            for i in self.coords:
                if touchingSettled == False and self.matrix[i[1]][i[0] - 1] == 1:
                    touchingSettled = True
            if touchingSettled == False:
                self.coords = [(i[0] - 1, i[1]) for i in self.coords]
    
    def CheckLoss(self):
        if 1 in self.matrix[0]:
            sys.exit()

class Screen():
    """Purpose: The main screen for pygame, where all objects are held.
    Attributes: width (int), height (int), and caption (str).
    Methods: initiateDisplay(), and display()."""
    def __init__(self):
        self.width = 1400
        self.height = 1400
        self.caption = "Tetris"
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.tickrate = 15
        self.fillcolor = (0,0,0)
    def InitiateDisplay(self):
        pygame.display.set_caption(self.caption)
    def Display(self):
        pygame.display.update()
        self.screen.fill(self.fillcolor)
        self.clock.tick(self.tickrate)
    def Blit(self, sprite, x, y):
        self.screen.blit(sprite, (x,y))

# Setting up pygame
pygame.init()

# Initiate Screen Class Object
screen = Screen()
screen.InitiateDisplay()
crashed = False

bag = TetrominoBag()
bag.MakeDoubleBag()
grid = Grid(width, height, bag)

while not crashed:
    # Some procedural thing that must be included for pygame to run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    # Rendering Blocks
    for h in range(len(grid.matrix)):
        for w in range(len(grid.matrix[0])):
            if grid.matrix[h][w] != 0:
                pygame.draw.rect(screen.screen, (255,255,255), (w * 50, h * 50, 50, 50))
    
    # Grid Activities
    grid.NewBlock()
    grid.BlockToMatrix()
    grid.MoveBlock()
    grid.BlockNaturalDrop()
    grid.CheckLoss()
    screen.clock.tick(screen.tickrate)
    pprint.pprint(grid.matrix)

    # Displaying the screen
    screen.Display()

pygame.display.quit()
sys.exit()
