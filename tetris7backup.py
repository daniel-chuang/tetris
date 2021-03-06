# Tetris
"""The game of tetris!
Version 1: CLI Block Selection and Dropping
Version 2: Pygame Interface, Game Loss Detection, Block Movement
Version 3: Instant Drop, Slow Drop, Left Right Movement
Version 4 (NON-FUNCTIONAL): Reworked Coordinate System for Tetrominos. Now there is rotations,
but left and right movement doesn't work anymore. The game is very buggy and crashes.
Version 5: Backstep on the rework coordinate system and restart.
Fixed left and right movement issue, and fixed the bugs and crashes. The game
uses both matrix and tuples now for tetrominos!
Version 6: Row Deletion, smooth controls, slower drops, rotations working other than wall kicks.
A very simple scoring system works, and the score is rendered on the top left on the screen.

TO-DO:
-Improve quick tap controls
-Make better immediate drop function
-Wall kick rotations
-Check over everything to make it run smoothly.
-Pylint + simplify redundant code
-Add color
-Make Tetris Grid
-Make levels and improve scoring https://tetris.fandom.com/wiki/Scoring
https://tetris.wiki/Tetris_(NES,_Nintendo)#:~:text=Start%20at%20level%2012%2C%20advance,level%2018%20at%20120%20lines.
-Add music
-Publish Game"""

# Imports
import sys
import pprint
import random
import time
import pygame
# For score text stuff https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
import pygame.freetype
import numpy as np

# Data
WIDTH = 10
HEIGHT = 22
BLOCKSIZE = 30

# Functions
def rotate_matrix(matrix):
    """Rotates a matrix 90 degrees"""
    return np.rot90(matrix)

# Classes
class Tetromino():
    """Tetris is a game of dropping blocks on a grid. These blocks are also called tetrominos.
    This class makes Tetrominos in matrixes."""
    def __init__(self, x, y, block_dropping_type):
        """Attributes for class."""
        self.matrix = []
        self.x = x
        self.y = y
        self.block_dropping_type = block_dropping_type
        self.coords = []

    def tetromino_to_matrix(self):
        """Returns a matrix with 0 denoting empty space and 2 denoting occupied space"""
        if self.block_dropping_type == "I":
            self.matrix = [
                            [0, 0, 0, 0],
                            [2, 2, 2, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]
                                        ]
        elif self.block_dropping_type == "J":
            self.matrix = [
                            [2, 0, 0],
                            [2, 2, 2],
                            [0, 0, 0]
                                        ]
        elif self.block_dropping_type == "L":
            self.matrix = [
                            [0, 0, 2],
                            [2, 2, 2],
                            [0, 0, 0]
                                        ]
        elif self.block_dropping_type == "O":
            self.matrix = [
                            [2, 2],
                            [2, 2]
                                    ]
        elif self.block_dropping_type == "Z":
            self.matrix = [
                            [0, 2, 2],
                            [2, 2, 0],
                            [0, 0, 0]
                                        ]
        elif self.block_dropping_type == "S":
            self.matrix = [
                            [2, 2, 0],
                            [0, 2, 2],
                            [0, 0, 0]
                                        ]
        elif self.block_dropping_type == "T":
            self.matrix = [
                            [0, 2, 0],
                            [2, 2, 2],
                            [0, 0, 0]
                                        ]
        return self.matrix

    def rotate_tetromino(self):
        """Rotates the tetromino"""
        self.matrix = rotate_matrix(self.matrix)
        return self.matrix

    def tetromino_to_tuples(self):
        """Returns a list of tuples (ordered pairs) for tetromino coordinates."""
        self.coords = []
        for i in range(len(self.matrix)):
            for z in range(len(self.matrix[i])):
                if self.matrix[i][z] != 0:
                    self.coords.append((z + self.x, i + self.y))
        return self.coords

    def convert_to_settled(self):
        """Turns all the 2s in the matrix to 1"""
        for i in range(len(self.matrix)):
            for z in range(len(self.matrix[i])):
                if self.matrix[i][z] == 2:
                    self.matrix[i][z] = 1
        return self.matrix

class TetrominoBag():
    """Tetris Worlds uses a 2 (14 blocks) bag system. This class replicates that."""
    def __init__(self):
        """Attributes for class."""
        self.bag = {}
        self.tetromino_type_list = ["I", "J", "L", "O", "S", "T", "Z"]

    def MakeDoubleBag(self):
        """Makes a bag of 2 of each tetromino type."""
        for i in self.tetromino_type_list :
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
        self.block_dropping_type = ""
        self.score = 0

    def NewBlock(self):
        """Creates a new block and returns the starting coordinates for that block."""
        for i in self.matrix:
            if 2 in i:
                return
        self.block_dropping_type = self.bag.Choose()
        self.tetromino = Tetromino(round(self.width/2), 0, self.block_dropping_type)
        self.tetromino.tetromino_to_matrix()
        self.coords = self.tetromino.tetromino_to_tuples()
        return self.coords

    def BlockToMatrix(self):
        """Updates the matrix with the block."""
        self.coords = self.tetromino.tetromino_to_tuples()
        for h in range(HEIGHT):
            for w in range(WIDTH):
                if self.matrix[h][w] == 2:
                    self.matrix[h][w] = 0
        for i in self.coords:
            self.matrix[i[1]][i[0]] = 2

    def BlockNaturalDrop(self):
        """Block dropping due to gravity."""
        self.coords = self.tetromino.tetromino_to_tuples()
        # Checks for collision
        for i in self.coords:
            if i[1] == self.height - 1:
                for i in self.coords:
                    self.matrix[i[1]][i[0]] = 1
                return
            if self.matrix[i[1] + 1][i[0]] == 1:
                for i in self.coords:
                    self.matrix[i[1]][i[0]] = 1
                return
        self.tetromino.y += 1
        Grid.BlockToMatrix(self)

    def RotateBlock(self):
        """Rotates the block that is currently dropping"""
        self.tetromino.rotate_tetromino()
        """self.coords = self.tetromino.tetromino_to_tuples()
        for i in self.coords:
            if i in """
        return

    def MoveBlock(self, frame):
        """Allows for the user to press left and right to move the blocks."""
        self.coords = self.tetromino.tetromino_to_tuples()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and WIDTH - 1 not in [i[0] for i in self.coords]:
            touchingSettled = False
            for i in self.coords:
                if touchingSettled == False and self.matrix[i[1]][i[0] + 1] == 1:
                    touchingSettled = True
            if touchingSettled == False:
                self.tetromino.x += 1
            Grid.BlockToMatrix(self)
        if keys[pygame.K_LEFT] and 0 not in [i[0] for i in self.coords]:
            touchingSettled = False
            for i in self.coords:
                if touchingSettled == False and self.matrix[i[1]][i[0] - 1] == 1:
                    touchingSettled = True
            if touchingSettled == False:
                self.tetromino.x -= 1
            Grid.BlockToMatrix(self)
        if keys[pygame.K_DOWN]: # Slow drop
            for i in range(2):
                Grid.BlockNaturalDrop(self)
        if keys[pygame.K_SPACE]: # Fast drop
            for i in range(10):
                Grid.BlockNaturalDrop(self)
        if keys[pygame.K_TAB] and frame % 2 == 0:
            Grid.RotateBlock(self)
        return

    def CheckFullRow(self):
        """Checks if there has been a complete row in the game!"""
        for i in range(len(self.matrix)):
            if self.matrix[i] == [1 for x in range(self.width)]:
                del self.matrix[i]
                self.matrix.insert(0, [0 for x in range(self.width)])
                self.score += 100

    def CheckLoss(self):
        """Checks if the user has stacked tiles up to the top, and ends the game if that is true."""
        if 1 in self.matrix[1]:
            return True

class Screen():
    """Purpose: The main screen for pygame, where all objects are held.
    Attributes: width (int), height (int), and caption (str).
    Methods: initiateDisplay(), and display()."""
    def __init__(self):
        self.font = pygame.freetype.Font("OpenSans-Regular.ttf", 25)
        self.width = WIDTH * BLOCKSIZE
        self.height = HEIGHT * BLOCKSIZE
        self.caption = "Tetris"
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.tickrate = 20
        self.fillcolor = (0,0,0)
        self.frame = 0
    def InitiateDisplay(self):
        """Sets up the display."""
        pygame.display.set_caption(self.caption)
    def Display(self):
        """Displays the screen, pauses for frames, and fills the backdrop."""
        pygame.display.update()
        self.screen.fill(self.fillcolor)
        self.clock.tick(self.tickrate)
    def BlitText(self, text: str, coords: tuple, color: tuple):
        """Puts text onto the screen."""
        self.font.render_to(self.screen, coords, text, color)
    def BlitSprite(self, sprite, x, y):
        """Puts a sprite on the screen."""
        self.screen.blit(sprite, (x,y))

def main():
    # Setting up pygame
    pygame.init()

    # Initiate Screen Class Object
    screen = Screen()
    screen.InitiateDisplay()
    crashed = False

    bag = TetrominoBag()
    bag.MakeDoubleBag()
    grid = Grid(WIDTH, HEIGHT, bag)

    while not crashed:

        screen.frame += 1

        # Some procedural thing that must be included for pygame to run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        # Grid Activities
        grid.NewBlock()
        grid.BlockToMatrix()
        grid.MoveBlock(screen.frame)
        if screen.frame % 6 == 0:
            grid.BlockNaturalDrop()
        grid.CheckFullRow()

        # Rendering Blocks
        pygame.draw.rect(screen.screen, (255, 0, 0), (0, BLOCKSIZE * 2, WIDTH * BLOCKSIZE, 2))

        # Rendering Score
        screen.BlitText(str(grid.score), (10, 10), (255, 255, 255))

        for h in range(len(grid.matrix)):
            for w in range(len(grid.matrix[0])):
                if grid.matrix[h][w] != 0:
                    pygame.draw.rect(screen.screen, (255,255,255),
                    (w * BLOCKSIZE, h * BLOCKSIZE, BLOCKSIZE-1, BLOCKSIZE-1))

        # Continuing Grid Activities
        if grid.CheckLoss():
            break
        screen.clock.tick(screen.tickrate)

        # Displaying the screen
        screen.Display()

    time.sleep(3)
    pygame.display.quit()
    sys.exit()
main()
