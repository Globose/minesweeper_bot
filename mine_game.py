"""Minesweeper library"""

import time
import random
import numpy as np
import cv2
import pyautogui

pyautogui.PAUSE = 0

def screenshot():
    """Takes a screenshot of the screen and returns it"""
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image


def is_grey(color):
    """Returns true if color is grey"""
    return ((164 < color[0] < 192) and
            (164 < color[1] < 192) and (164 < color[2] < 192))


def same_color(color_1, color_2):
    """Returns true if two colors the same or almost the same"""
    for c1, c2 in zip(color_1, color_2):
        if c1-2 > c2 or c2 > c1+2:
            return False
    return True


def mouse_left(x, y):
    """Left mouse click on x,y"""
    pyautogui.leftClick(x, y)


def find_gray_dots(image):
    """Looks for some gray pixels in the image"""
    tiles = []
    for x in range(0, len(image[0]), 10):
        for y in range(0, len(image), 10):
            if is_grey(image[y, x]):
                tiles.append(Tile(x, y, image[y, x]))
    return tiles


def find_tiles(image):
    """Searches for grey tiles in the image"""
    tiles = find_gray_dots(image)

    for t in tiles:
        t.move_dot(image)

    for i, tile_0 in enumerate(tiles):
        for j, tile_1 in enumerate(tiles[:]):
            if (tile_0.position() == tile_1.position() and tile_0 != tile_1):
                tiles.remove(tile_1)

    for t in tiles:
        t.expand(image)

    for i, tile in enumerate(tiles[:]):
        if tile.size < 4:
            tiles.remove(tile)

    return tiles


def create_games(tiles):
    """Creates a list of class Game from seperate squares"""
    columns = []
    while len(tiles) != 0:
        temp_tile = tiles.pop(0)
        column_0 = [temp_tile]
        tile_added = True
        while tile_added:
            tile_added = False
            for t in tiles:
                if (t.x == temp_tile.x and
                        t.y > column_0[-1].y+column_0[-1].size*1.2 and
                        t.y < column_0[-1].y+2*column_0[-1].size):
                    column_0.append(t)
                    tiles.remove(t)
                    tile_added = True
                    break
        columns.append(column_0)

    games = []
    while len(columns) != 0:
        column_0 = columns.pop(0)
        board = [column_0]
        column_added = True
        while column_added:
            column_added = False
            for c in columns:
                if (c[0].y == column_0[0].y and len(c) == len(column_0) and
                        c[0].x > board[-1][0].x + board[-1][0].size and
                        c[0].x < board[-1][0].x + 2 * board[-1][0].size):
                    board.append(c)
                    columns.remove(c)
                    column_added = True
                    break
        if len(board) > 7:
            games.append(Game(board))
    return games


def non_flagged(tile):
    """Returns a list of unknown neigbour tiles"""
    tile_non_flagged = []
    for n in tile.neigh:
        if n.type_hidden == 10:
            tile_non_flagged.append(n)
    return tile_non_flagged


def flagged(tile):
    """Returns a list of flagged neighbour tiles"""
    tile_flagged = []
    for n in tile.neigh:
        if n.type_hidden == 0:
            tile_flagged.append(n)
    return tile_flagged


def diff(set_a, set_b):
    """Returns the difference of set A and B"""
    set_c = []
    for f1 in set_a:
        if f1 not in set_b:
            set_c.append(f1)
    return set_c


def solve_pairs(tile_a, tile_b):
    """Algorithm to find solutions given two tiles"""
    not_flagged_a = non_flagged(tile_a)
    not_flagged_b = non_flagged(tile_b)
    a_value = tile_a.type_hidden - len(flagged(tile_a))
    b_value = tile_b.type_hidden - len(flagged(tile_b))

    if a_value - b_value == len(diff(not_flagged_a, not_flagged_b)):
        for t in diff(not_flagged_a, not_flagged_b):
            t.type_hidden = 0
            for n in t.neigh:
                n.update()
        for t in diff(not_flagged_b, not_flagged_a):
            t.type_hidden = 9
            for n in t.neigh:
                n.update()


def get_guess_tile(board):
    """Returns a tile to guess on"""
    lst = []
    for col in board:
        for s in col:
            if s.type_hidden == 10:
                lst.append(s)
    lst2 = []
    for s in lst:
        for n in s.neigh:
            if 9 > n.type_hidden > 0:
                lst2.append(s)
                break

    if len(lst2) > 0:
        return lst2[random.randrange(len(lst2))]
    elif len(lst) > 0:
        return lst[random.randrange(len(lst))]
    else:
        return None


class Tile:
    """Class for the game tiles"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 1
        self.type_visual = 10
        self.type_hidden = 10
        self.neigh = []
        self.COLORS = [[0, 127, 255], [250, 0, 0], [0, 200, 0],
                       [0, 0, 250], [100, 20, 20], [30, 30, 90],
                       [100, 100, 20], [20, 20, 20], [100, 100, 100],
                       [255, 255, 0], [255, 255, 255]]

    def move_dot(self, image):
        """Moves the dot up left as long as the color is similar"""
        current_color = image[self.y, self.x]
        moved = True
        while moved:
            moved = False
            for i in range(self.x-1, 0, -1):
                if same_color(current_color, image[self.y, i]):
                    self.x = i
                    moved = True
                else:
                    break

            for i in range(self.y-1, 0, -1):
                if same_color(current_color, image[i, self.x]):
                    self.y = i
                    moved = True
                else:
                    break

    def position(self):
        """Returns the position of the tile"""
        return (self.x, self.y)

    def expand(self, image):
        """Expands the tiles' size"""
        while (self.size+self.y < len(image) and
               self.size+self.x < len(image[0])):
            x_ok = same_color(self.color, image[self.y, self.x+self.size])
            y_ok = same_color(self.color, image[self.y+self.size, self.x])
            d_ok = same_color(self.color, image[self.y+self.size,
                                                self.x+self.size])
            if not (x_ok and y_ok and d_ok):
                break
            self.size += 1

    def reset(self):
        """Resets the value data of the tile"""
        self.type_visual = 10
        self.type_hidden = 10

    def click(self):
        """Mouse click on the tile"""
        pyautogui.leftClick(self.x+self.size/2, self.y+self.size/2)

    def update(self):
        """Looks if there is an update to the tile"""
        if self.type_hidden < 1 or self.type_hidden > 9:
            return
        fnd_bombs = 0
        unknown = 0

        for n in self.neigh:
            if n.type_hidden == 0:
                fnd_bombs += 1
            elif n.type_visual == 10 and n.type_hidden == 10:
                unknown += 1

        if fnd_bombs == self.type_hidden:
            for n in self.neigh:
                if n.type_hidden == 10:
                    n.type_hidden = 9
        elif unknown == self.type_hidden - fnd_bombs:
            for n in self.neigh:
                if n.type_hidden == 10:
                    n.type_hidden = 0
                    for nn in n.neigh:
                        nn.update()

    def update_visual(self, image):
        """Looks if the tile has changed visually"""
        colors = []
        for i in range(0, 6):
            for j in range(0, 6):
                colors.append(image[self.y+j*self.size//6-2,
                                    self.x+i*self.size // 6-2])

        if colors[0][0] < 70 and colors[0][1] < 70 and colors[0][2] > 180:
            self.type_visual = self.type_hidden = -1
            return

        value = 9
        for col in colors:
            if col[0] > 235 and col[2] < 80:
                value = 1
            elif col[0] < 15 and col[1] > 100 and col[2] < 40:
                value = 2
            elif col[0] < 50 and col[2] > 225:
                value = 3
            elif 150 > col[0] > 100 and col[2] < 15:
                value = 4
            elif col[0] < 15 and col[1] < 15 and col[2] > 100:
                value = 5
            elif col[0] > 100 and col[1] > 100 and col[2] < 40:
                value = 6
            elif col[0] < 15 and col[1] < 15 and col[2] < 15:
                value = 7
            elif (110 < col[0] < 134 and 110 < col[1] < 134 and
                  110 < col[2] < 134):
                value = 8
            elif col[0] > 195 and col[1] > 195 and col[2] > 195:
                value = 10

            if value < 9:
                break

        if value != self.type_visual:
            self.type_visual = value
            self.type_hidden = value
            for n in self.neigh:
                n.update_visual(image)


class Game:
    """Class that manages different boards"""
    def __init__(self, board):
        self.board = board
        self.solved = False
        for i, column in enumerate(board):
            for j, tile in enumerate(column):
                for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                        if (x != i or y != j) and (0 <= x < len(board) and
                                                   0 <= y < len(board[0])):
                            tile.neigh.append(board[x][y])

    def reset(self):
        """Resets the board and clicks the reset button"""
        x = self.board[int(len(self.board)/2)][0].x
        y = self.board[0][0].y - self.board[0][0].size*2
        mouse_left(x, y)

        for column in self.board:
            for tile in column:
                tile.reset()

    def solve_game(self):
        """Solves the game"""
        last_mouse = 0
        new_game = True
        click_tiles = []

        while True:
            if new_game:
                last_mouse = 0
                self.reset()
                click_tiles = [self.board[len(self.board)//2][len(self.board[0])//2]]
                new_game = False
                
            current_mouse = pyautogui.position().x
            if last_mouse != current_mouse and last_mouse != 0:
                break

            for t in click_tiles:
                t.click()
            last_mouse = pyautogui.position().x

            time.sleep(0.07)
            image = screenshot()
            
            for t in click_tiles:
                t.update_visual(image)

                if t.type_hidden == -1:
                    new_game = True
                    

            if new_game:
                continue

            click_tiles = []
            for column in self.board:
                for tile in column:
                    if 0 < tile.type_hidden < 9:
                        tile.update()

            for column in self.board:
                for tile in column:
                    if 0 < tile.type_hidden < 9:
                        for n in tile.neigh:
                            if 0 < n.type_hidden < 9:
                                solve_pairs(tile, n)

            for column in self.board:
                for tile in column:
                    if tile.type_hidden == 9 and tile.type_visual == 10:
                        click_tiles.append(tile)

            if len(click_tiles) == 0:
                tile_guess = get_guess_tile(self.board)
                if tile_guess is None:
                    break
                click_tiles.append(tile_guess)

            