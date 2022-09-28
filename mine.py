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

    def get_position(self):
        return [self.y,self.x]

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

class Board:
    def __init__(self, board, bombs, button_pos):
        self.board = board
        self.bombs = bombs
        self.button_pos = button_pos
        
    def right_click_all(self):
        for column in self.board:
            for square in column:
                pyautogui.rightClick(square.x+square.size/2,
                    square.y+square.size/2)
    
def is_grey(rgb):
    return (164 < rgb[0] < 194) and (164 < rgb[1] < 194) and (164 < rgb[2] < 194)

def screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    return image

def find_gray_dots(image):
    squares = []
    for y in range(0,len(image),10):
        for x in range(0,len(image[0]),10):
            if is_grey(image[y,x]):
                squares.append(Square(x,y,image[y,x]))

    return squares

def mouse_right(x,y):
    pyautogui.rightClick(x,y)

def save_image(image, filename="image.png"):
    cv2.imwrite(filename, image)

def create_boards(squares):
    columns = []
    boards = []
    for s in squares:
        row = [s]
        last_y = s.y
        col_x = s.x
        for s2 in squares[:]:
            if s2.size == s.size and s2.x == col_x and \
                s2.y > last_y+s.size and s2.y < last_y+2*s.size:
                    row.append(s2)
                    last_y = s2.y
                    squares.remove(s2)

        columns.append(row)
    
    for c in columns:
        board = [c]
        row_y = c[0].y
        last_x = c[0].x
        c_size = c[0].size
        for c2 in columns[:]:
            if row_y == c2[0].y and last_x + c_size < c2[0].x and \
                last_x+2*c_size > c2[0].x and c_size == c2[0].size and \
                    len(c2) == len(c):
                        board.append(c2)
                        last_x = c2[0].x
                        columns.remove(c2)
        if (len(board) > 7):
            boards.append(board)
    
    boards_c = []
    for b in boards:
        boards_c.append(Board(b,-1,(100,100)))
    return boards_c

def main():
    image = screenshot()
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

    for s in squares:
        s.paint_square(image)

    print(len(squares))
    boards = create_boards(squares)
    print(len(boards))
    for b in boards:
        b.right_click_all()
    save_image(image)

if __name__ == '__main__':
    main()
