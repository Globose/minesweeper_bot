import numpy as np
import cv2
import pyautogui

class Square:
    """Square"""
    def __init__(self, x_pos,y_pos, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.width = 1
        self.height = 1

    def move_dot(self, image):
        current_color = image[self.x_pos,self.y_pos]
        for i in range(self.x_pos, 0, -1):
            if (current_color == image[i,self.y_pos]).all():
                self.x_pos = i
            else:
                break
        
        for i in range(self.y_pos, 0, -1):
            if (current_color == image[self.x_pos,i]).all():
                self.y_pos = i
            else:
                break
    
    def paint_dot(self, image):
        image[self.x_pos, self.y_pos] = [0, 0, 255]
    
    def paint_square(self, image):
        for i in range(self.x_pos,self.x_pos+self.width):
            image[i,self.y_pos] = [0, 0, 255]

        for j in range(self.y_pos,self.y_pos+self.height):
            image[self.x_pos,j] = [0, 0, 255]

    def get_position(self):
        return [self.x_pos,self.y_pos]

    def expand(self, image):
        for i in range(self.x_pos,len(image)):
            if (image[i,self.y_pos]==self.color).all():
                self.width += 1
                continue
            break
        
        for i in range(self.y_pos,len(image[0])):
            if (image[self.x_pos,i]==self.color).all():
                self.height += 1
                continue
            break

def is_grey(rgb):
    return (164 < rgb[0] < 194) and (164 < rgb[1] < 194) and (164 < rgb[2] < 194)

def screenshot():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    return image

def find_gray_dots(image):
    squares = []
    for y in range(0,len(image[0]),10):
        for x in range(0,len(image),10):
            if is_grey(image[x,y]):
                squares.append(Square(x,y,image[x,y]))

    return squares

def mouse_left(x,y):
    pyautogui.click(x,y)

def save_image(image):
    cv2.imwrite("image.png", image)

def main():
    image = screenshot()
    squares = find_gray_dots(image)

    for s in squares:
        s.move_dot(image)

    for s1 in squares:
        for s2 in squares:
            if s1 != s2 and s1.get_position() == s2.get_position():
                squares.remove(s2)
    
    for s1 in squares:
        s1.expand(image)

    for s in squares:
        s.paint_square(image)

    save_image(image)

if __name__ == '__main__':
    main()
