import numpy as np
import cv2
import pyautogui

class Square:
    """Square"""
    def __init__(self, x_pos,y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos


def is_grey(rgb):
    return (164 < rgb[0] < 194) and (164 < rgb[1] < 194) and (164 < rgb[2] < 194)

image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)

squares = []
for y in range(0,len(image[0]),8):
    for x in range(0,len(image),8):
        if is_grey(image[x,y]):
            image[x,y] = [0,0,255]
            squares.append(Square(x,y))



#pyautogui.click(150,350)

cv2.imwrite("image1.png", image)

