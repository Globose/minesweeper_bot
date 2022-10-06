import numpy as np
import cv2
import pyautogui
import time
import square
from square import is_grey, screenshot, find_gray_dots, mouse_left, save_image,create_games,find_squares

def solve_games(games):
    pyautogui.PAUSE = 0
    for game in games:
        game.solve_game()
    
    image = screenshot()
    for game in games:
        game.draw_game(image)
    save_image(image)

def main():
    image = screenshot()
    squares = find_squares(image)
    games = create_games(squares, image)
    solve_games(games)


if __name__ == '__main__':
    main()

