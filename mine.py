import numpy as np
import cv2
import pyautogui
import time
import square
from square import is_grey, screenshot, find_gray_dots, mouse_left, save_image,create_games,find_squares

def solve_games(games):
    for game in games:
        start_sq = game.board[len(game.board)//2][len(game.board[0])//2]
        start_sq.click()
        image = screenshot()
        start_sq.update(image)
        game.draw_game(image)
        save_image(image)

def main():
    image = screenshot()
    squares = find_squares(image)
    games = create_games(squares)
    solve_games(games)

if __name__ == '__main__':
    main()

