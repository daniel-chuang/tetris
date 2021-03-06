# Tetris
"""The game of tetris!
Version 1: CLI Block Selection and Dropping
Version 2: Pygame Interface, Game Loss Detection, Block Movement
Version 3: Instant Drop, Slow Drop, Left Right Movement
Version 4: Reworked Coordinate System for Tetrominos. Now there is rotations, but left and right movement doesn't work anymore.

TO-DO:
Fix left and right movement.
Check over everything to make it run smoothly.
Make row deletion + scoring
Add color
Add music
Publish Game"""

# Imports
import sys
import pprint
import random
import pygame
import time
import numpy as np

# Data
width = 10
height = 22
blocksize = 30

# Functions
def RotateMatrix(matrix):
    """Rotates a matrix 90 degrees"""
    return(np.rot90(matrix))

# Classes
class Tetromino():
    """Tetris is a game of dropping blocks on a grid. These blocks are also called tetrominos. This class makes Tetrominos in matrixes."""
    def __init__(self, x, y, blockDroppingType):
        """Attributes for class."""
        self.matrix = []
        self.x = x
        self.y = y
        self.blockDroppingType = blockDroppingType

    def TetrominoToMatrix(self):
        """Returns a matrix with 0 denoting empty space and 2 denoting occupied space"""
        if self.blockDroppingType == "I":
            self.matrix = [
                            [0, 0, 0, 0],
                            [2, 2, 2, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]
                                        ]
        elif self.blockDroppingType == "J":
            self.matrix = [
                            [2, 0, 0],
                            [2, 2, 2],
                            [0, 0, 0]
                                        ]
        elif self.blockDroppingType == "L":
            self.matrix = [
                            [0, 0, 2],
                            [2, 2, 2],
                            [0, 0, 0]
                                        ]
        elif self.blockDroppingType == "O":
            self.matrix = [
                            [2, 2],
                            [2, 2]
                                    ]
        elif self.blockDroppingType == "Z":
            self.matrix = [
                            [0, 2, 2],
                            [2, 2, 0],
                            [0, 0, 0]
                                        ]
        elif self.blockDroppingType == "S":
            self.matrix = [
                            [2, 2, 0],
                            [0, 2, 2],
                            [0, 0, 0]
                                        ]
        elif self.blockDroppingType == "T":
            self.matrix = [
                            [0, 2, 0],
                            [2, 2, 2],
                            [0, 0, 0]
                                        ]
        return

    def RotateTetromino(self):
        """Rotates the tetromino"""
        self.matrix = RotateMatrix(self.matrix)
        return

    def ConvertToSettled(self):
        """Turns all the 2s in the matrix to 1"""
        for i in range(len(self.matrix)):
            for z in range(len(self.matrix[i])):
                if self.matrix[i][z] == 2:
                    self.matrix[i][z] = 1

class TetrominoBag():
    """Tetris Worlds uses a 2 (14 blocks) bag system. This class replicates that."""
    def __init__(self):
        """Attributes for class."""
        self.bag = {}
        self.tetrominoTypeList = ["I", "J", "L", "O", "S", "T", "Z"]

    def MakeDoubleBag(self):
        """Makes a bag of 2 of each tetromino type."""
        for i in self.tetrominoTypeList:
            self.bag.update({i : 2})

    def Choose(self):
        """Returns a choice from the bag, and removes that block from the bag."""
        if self.bag == {}:
            TetrominoBag.MakeDoubleBag(self)
        lst = [x for x in self.bag.keys()]
        choice = random.choices(lst, k=1)[0]
        if self.bag.get(choice) == 1:
            self.bag.pop(choice)
        else:
            self.bag.update({choice : self.bag.get(choice) - 1})
        return choice

class Grid():
    """Represents the tetris grids and the blocks on it."""
    def __init__(self, width, height, bag):
        """Attributes for class"""
        self.matrix = [[0 for z in range(width)] for i in range(height)]
        """0 means block is empty. 1 means the block is settled. 2 means the block is dropping."""
        self.colorMatrix = [[(0,0,0) for z in range(width)] for i in range(height)]
        self.width = width
        self.height = height
        self.coords = ""
        self.bag = bag
        self.blockDimensions = {"I" : 4, "J" : 3, "L" : 3, "O" : 2, "S" : 3, "T" : 3, "Z": 3}
        self.blockDroppingType = ""

    def NewBlock(self):
        """Creates a new tetromino block on the grid!"""
        for i in self.matrix: # checks if there is already a block dropping
            if 2 in i:
                return()
        self.blockDroppingType = self.bag.Choose()
        self.tetromino = Tetromino(round(self.width/2), 0, self.blockDroppingType)
        self.tetromino.TetrominoToMatrix()

    def BlockToMatrix(self):
        """Updates the matrix with the block and clears the previous position."""
        for h in range(height):
            for w in range(width):
                if self.matrix[h][w] == 2:
                    self.matrix[h][w] = 0
        for i in range(len(self.tetromino.matrix)):
            for z in range(len(self.tetromino.matrix[i])):
                self.matrix[i + self.tetromino.y][z + self.tetromino.x] = self.tetromino.matrix[i][z]

    def BlockNaturalDrop(self):
        """Block dropping due to gravity."""
        # Checks for collision
        if 2 in self.matrix[height - 1]:
            self.tetromino.ConvertToSettled()
            Grid.NewBlock(self)
            return()
        for i in range(len(self.tetromino.matrix)):
            for z in range(len(self.tetromino.matrix[i])):
                if 1 in self.tetromino.matrix[i] or 2 in self.tetromino.matrix[i]:
                    if self.matrix[i + self.tetromino.y + 1][z + self.tetromino.x] == 1:
                        self.tetromino.ConvertToSettled()
                        return()
        self.tetromino.y += 1
        Grid.BlockToMatrix(self)

    def MoveBlock(self):
        """Allows for the user to press left and right to move the blocks."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.tetromino.matrix
        elif keys[pygame.K_LEFT] and 0 not in [i[0] for i in self.coords]:
            touchingSettled = False
            for i in self.coords:
                if touchingSettled == False and self.matrix[i[1]][i[0] - 1] == 1:
                    touchingSettled = True
            if touchingSettled == False:
                self.coords = [(i[0] - 1, i[1]) for i in self.coords]
            Grid.BlockToMatrix(self)
        elif keys[pygame.K_DOWN]: # Slow drop
            for i in range(2):
                Grid.BlockNaturalDrop(self)
        elif keys[pygame.K_SPACE]: # Fast drop
            for i in range(20):
                Grid.BlockNaturalDrop(self)
        elif keys[pygame.K_TAB]:
            self.tetromino.RotateTetromino()

    def CheckLoss(self):
        """Checks if the user has stacked tiles up to the top, and ends the game if that is true."""
        if 1 in self.matrix[1]:
            return(True)

class Screen():
    """Purpose: The main screen for pygame, where all objects are held.
    Attributes: width (int), height (int), and caption (str).
    Methods: initiateDisplay(), and display()."""
    def __init__(self):
        self.width = width * blocksize
        self.height = height * blocksize
        self.caption = "Tetris"
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.tickrate = 15
        self.fillcolor = (0,0,0)
    def InitiateDisplay(self):
        """Sets up the display."""
        pygame.display.set_caption(self.caption)
    def Display(self):
        """Displays the screen, pauses for frames, and fills the backdrop."""
        pygame.display.update()
        self.screen.fill(self.fillcolor)
        self.clock.tick(self.tickrate)
    def Blit(self, sprite, x, y):
        """Puts a sprite on the screen."""
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

    # Grid Activities
    grid.NewBlock()
    grid.BlockToMatrix()
    grid.MoveBlock()
    grid.BlockNaturalDrop()

    # Rendering Blocks
    pygame.draw.rect(screen.screen, (255, 0, 0), (0, blocksize * 2, width * blocksize, 2))

    for h in range(len(grid.matrix)):
        for w in range(len(grid.matrix[0])):
            if grid.matrix[h][w] != 0:
                pygame.draw.rect(screen.screen, (255,255,255), (w * blocksize, h * blocksize, blocksize-1, blocksize-1))
    
    # Continuing Grid Activities
    if grid.CheckLoss():
        break
    #pprint.pprint(grid.matrix)
    screen.clock.tick(screen.tickrate)
    print()

    # Displaying the screen
    screen.Display()

time.sleep(3)
pygame.display.quit()
sys.exit()
