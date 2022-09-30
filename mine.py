import numpy as np
import cv2
import pyautogui
import time

class Square:
    """Square"""
    def __init__(self, x,y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 1
        self.open = False
        #types: (1-8) siffror, (0) bomb, (-1) ingenitng
        self.type = None
        self.neigh = []

    def move_dot(self, image):
        current_color = image[self.y,self.x]
        moved = True
        while moved:
            moved = False
            for i in range(self.x-1, 0, -1):
                if (current_color == image[self.y,i]).all():
                    self.x = i
                    moved = True
                else:
                    break
            
            for i in range(self.y-1, 0, -1):
                if (current_color == image[i,self.x]).all():
                    self.y = i
                    moved = True
                else:
                    break
    
    def paint_dot(self, image):
        image[self.y, self.x] = [0, 0, 255]
    
    def paint_square(self, image):
        for i in range(self.size):
            image[i+self.y,self.x] = [0, 0, 255]
            image[i+self.y,i+self.x] = [0, 0, 255]
            image[self.y,self.x+i] = [0, 0, 255]
            
    def paint_neigh(self, image):
        for n in self.neigh:
            n.paint_square(image)

    def get_position(self):
        return [self.x,self.y]

    def expand(self, image):
        while self.size+self.y < len(image) and self.size+self.x < len(image[0]):
            x_ok = (image[self.y,self.x+self.size]==self.color).all()
            y_ok = (image[self.y+self.size, self.x]==self.color).all()
            d_ok = (image[self.y+self.size,self.x+self.size]==self.color).all()
            if not (x_ok and y_ok and d_ok):
                break
            self.size +=1
            
    def draw_big(self,image):
        for x in range(0,10):
            for y in range(0,10):
                image[self.y+y,self.x+x] = [0,0,255]
                
    def click(self):
        pyautogui.leftClick(self.x+self.size/2,self.y+self.size/2)

class Game:
    def __init__(self, board, bombs, button_pos):
        self.board = board
        self.bombs = bombs
        self.solved = False
        self.button_pos = button_pos
        for i, col in enumerate(board):
            for j, sq in enumerate(col):
                for k in range(i-1, i+2):
                    for l in range(j-1, j+2):
                        if (k != i or l != j) and (0 <= k < len(board) and 0 <= l < len(board[0])):
                            sq.neigh.append(board[k][l])

def is_grey(rgb):
    return (164 < rgb[0] < 194) and (164 < rgb[1] < 194) and (164 < rgb[2] < 194)

def screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    return image

def find_gray_dots(image):
    squares = []
    for x in range(0,len(image[0]),10):
        for y in range(0,len(image),10):
            if is_grey(image[y,x]):
                squares.append(Square(x,y,image[y,x]))

    return squares

def mouse_left(x,y):
    pyautogui.leftClick(x,y)

def save_image(image, filename="image.png"):
    cv2.imwrite(filename, image)    

def create_games(squares):
    cols = []
    while len(squares) != 0:
        square = squares.pop(0)
        col = [square]
        square_added = True
        while square_added:
            square_added = False
            for s in squares:
                if (s.x == square.x and
                    s.y > col[-1].y+col[-1].size and s.y < col[-1].y+2*col[-1].size):
                    col.append(s)
                    squares.remove(s)
                    square_added = True
                    break
        cols.append(col)
    
    games = []
    while len(cols) != 0:
        col = cols.pop(0)
        board = [col]
        col_added = True
        while col_added:
            col_added = False
            for c in cols:
                if (c[0].y == col[0].y and len(c)==len(col) and
                        c[0].x > board[-1][0].x+board[-1][0].size and
                        c[0].x < board[-1][0].x+2*board[-1][0].size):
                    board.append(c)
                    cols.remove(c)
                    col_added = True
                    break
        if len(board) > 7:
            games.append(Game(board,10,(10,10)))
    return games

def find_squares(image):
    squares = find_gray_dots(image)
    
    for s in squares:
        s.move_dot(image)

    for i, s1 in enumerate(squares):
        for j,s2 in enumerate(squares[:]):
            if s1.get_position() == s2.get_position() and s1 != s2:
                squares.remove(s2)

    for s1 in squares:
        s1.expand(image)

    for i,s in enumerate(squares[:]):
        if s.size < 4:
            squares.remove(s)

    return squares

def solve_games(games):
    for game in games:
        start_sq = game.board[len(game.board)//2][len(game.board[0])//2]
        start_sq.click()

def main():
    image = screenshot()
    squares = find_squares(image)
    
    games = create_games(squares)
    solve_games(games)
    
    save_image(image)

if __name__ == '__main__':
    main()

