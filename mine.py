import numpy as np
import cv2
import pyautogui
import time
import square
from square import is_grey, screenshot, find_gray_dots, mouse_left, save_image,create_games,find_squares

def solve_games(games):
    for game in games:
        game.board[len(game.board)//2][len(game.board[0])//2].clik = True
    pyautogui.PAUSE = 0
    
    for game in games:
        for col in game.board:
            for sq in col:
                #sq.click()
                if sq.clik:
                    sq.click()
                    time.sleep(0.1)
                    image = screenshot()
                    sq.update_visual(image)
        game.draw_game(image)
    save_image(image)



def main():
    image = screenshot()
    squares = find_squares(image)
    
    games = create_games(squares, image)

    save_image(image)
    solve_games(games)


if __name__ == '__main__':
    main()

