from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time
import random

WIDTH = 16
HEIGHT = 16
MINES = 40

BOMB = 10
NONE = 0
CLOSED = 9


def get_Nr(class_name):
    """Returns number of square class"""
    if class_name == "square blank":
        return 9
    if class_name == "square bombdeath" or class_name == "square bombrevealed":
        return 10
    if class_name.find("open") != -1:
        return int(class_name[-1])
    return 0


def solve_pairs(tile_a, tile_b):
    """Algorithm to find solutions given two tiles"""
    closed_a = tile_a.get_adj_prop(CLOSED)
    closed_b = tile_b.get_adj_prop(CLOSED)
    
    value_a = tile_a.Nr - len(tile_a.get_adj_prop(BOMB))
    value_b = tile_b.Nr - len(tile_b.get_adj_prop(BOMB))

    if value_a - value_b == len(closed_a.difference(closed_b)):
        for tile in closed_a.difference(closed_b):
            tile.Nr = BOMB
            for a in tile.adj:
                a.update()
        for tile in closed_b.difference(closed_a):
            tile.Nr = CLOSED
            for a in tile.adj:
                a.update()


def get_guess_tile(board):
    """Returns a tile to guess on"""
    closedTiles = []
    for row in board:
        for tile in row:
            if tile.Nr == CLOSED:
                closedTiles.append(tile)
    adj_tiles = []
    for tile in closedTiles:
        for a in tile.adj:
            if 9 > a.Nr > 0:
                adj_tiles.append(tile)
                break

    if len(adj_tiles) > 0:
        return adj_tiles[random.randrange(len(adj_tiles))]
    elif len(closedTiles) > 0:
        return closedTiles[random.randrange(len(closedTiles))]
    else:
        return None


class Tile:
    """Tile classs"""
    def __init__(self, element):
        self.Nr = CLOSED
        self.vNr = CLOSED
        self.webElement = element
        self.adj = []

    def get_vNr(self):
        return get_Nr(self.webElement.get_attribute("class"))

    def click(self):
        self.webElement.click()
    
    def get_adj_prop(self, prop):
        adj_prop = []
        for tile in self.adj:
            if tile.Nr == prop:
                adj_prop.append(tile)
        return set(adj_prop)

    def update_vNr(self):
        vNr = self.get_vNr()
        if self.vNr != vNr:
            self.vNr = vNr
            self.Nr = vNr

    def update(self):
        if self.Nr < 1 or self.Nr > 9:
            return
        
        bombs = closed = 0
        for a in self.adj:
            if a.Nr == BOMB:
                bombs += 1
            elif a.Nr == CLOSED and a.vNr == CLOSED:
                closed += 1
        
        if bombs == self.Nr:
            for a in self.adj:
                if a.Nr == CLOSED:
                    a.Nr = NONE
                
        if self.Nr - bombs == closed:
            for a in self.adj:
                if a.Nr == CLOSED:
                    a.Nr = BOMB
                    for aa in a.adj:
                        a.update()


def init_chrome():   
    """Opens up a chrome window and returns the driver""" 
    service = Service("chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


def init_site(driver):
    driver.get("https://minesweeperonline.com/")
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "options-link")))
    gameOptions = driver.find_element(By.ID, "options-link")
    gameOptions.click()
    
    wait.until(EC.presence_of_element_located((By.ID, "custom")))
    radio = driver.find_element(By.ID, "custom")
    radio.click()
    
    heightBox = driver.find_element(By.ID, "custom_height")
    widthBox = driver.find_element(By.ID, "custom_width")
    minesBox = driver.find_element(By.ID, "custom_mines")

    heightBox.clear()
    widthBox.clear()
    minesBox.clear()
    
    heightBox.send_keys(HEIGHT)
    widthBox.send_keys(WIDTH)
    minesBox.send_keys(MINES)
    minesBox.submit()


def solve(board):
    """Solving function"""
    click_tiles = []
    new_game = True
    
    while True:
        if new_game:
            click_tiles.append(board[HEIGHT//2][WIDTH//2])
            new_game = False
        
        for tile in click_tiles:
            tile.click()

        for row in board:
            for tile in row:
                tile.update_vNr()
                if tile.vNr == BOMB:
                    new_game = True
                    break

        if new_game:
            break

        click_tiles = []
        for row in board:
            for tile in row:
                if 0 < tile.Nr < 9:
                    tile.update()

        for row in board:
            for tile in row:
                if 0 < tile.Nr < 9:
                    for a in tile.adj:
                        if 0 < a.Nr < 9:
                            solve_pairs(tile, a)

        for row in board:
            for tile in row:
                if tile.Nr == NONE and tile.vNr == CLOSED:
                    click_tiles.append(tile)
        
        # for row in board:
        #     for tile in row:
        #         print(tile.Nr, end=" ")
        #     print()
        
        if len(click_tiles) == 0:
            # print("make it up")
            tile_guess = get_guess_tile(board)
            if tile_guess is None:
                break
            click_tiles.append(tile_guess)
        # time.sleep(60)


def main():
    """Main Function"""
    driver = init_chrome()
    init_site(driver)
    board = np.full((HEIGHT, WIDTH), None)
    
    for i, row in enumerate(board):
        for j,_ in enumerate(row):
            board[i][j] = Tile(driver.find_element(By.ID, str(i+1)+"_"+str(j+1)))
    
    for i, row in enumerate(board):
        for j, tile in enumerate(row):
            for k in range(i-1, i+2):
                for m in range(j-1, j+2):
                    if (k != i or m != j) and (0 <= k < HEIGHT and 0 <= m < WIDTH):
                        tile.adj.append(board[k][m])
    
    solve(board)
    print("Done")
    time.sleep(1000)


if __name__ == "__main__":
    main()