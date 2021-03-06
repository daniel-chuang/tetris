# animation for medium article

from termcolor import colored
import time
import imageio
import pyautogui

pyautogui.FAILSAFE = True

matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
          [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
          [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

lst = set()
for i in range(21):
    for z in range(10):
        for row in range(len(matrix)):
            if 0 not in matrix[row]:
                lst.add(row)
            if (i == 20 or i > row) and row in lst:
                print(colored("1 " * 10, "green"))
            else:
                for element in range(len(matrix[row])):
                    if i == row and z == element:
                        print(colored(matrix[row][element], "green"), end=" ", flush=False)
                    elif matrix[row][element] == 1:
                        print(colored(matrix[row][element], "red"), end=" ", flush=False)
                    elif matrix[row][element] == 2:
                        print(colored(matrix[row][element], "blue"), end=" ", flush=False)
                    else:
                        print(matrix[row][element], end=" ", flush=False)
                print("")
        print("")
        # takes a screenshot
        pyautogui.moveTo(338, 580, duration = 0)
        pyautogui.hotkey('command', 'shift', '4')
        pyautogui.dragTo(547, 1000, duration = 0, button = 'left')
