import numpy as np
import cv2
import pyautogui

class Square:
    """Square"""
    def __init__(self, x,y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 1

    def move_dot(self, image):
        current_color = image[self.x,self.y]
        for i in range(self.x, 0, -1):
            if (current_color == image[i,self.y]).all():
                self.x = i
            else:
                break
        
        for i in range(self.y, 0, -1):
            if (current_color == image[self.x,i]).all():
                self.y = i
            else:
                break
    
    def paint_dot(self, image):
        image[self.x, self.y] = [0, 0, 255]
    
    def paint_square(self, image):
        for i in range(self.size):
            image[i+self.x,self.y] = [0, 0, 255]
            image[i+self.x,i+self.y] = [0, 0, 255]
            image[self.x,self.y+i] = [0, 0, 255]

    def get_position(self):
        return [self.x,self.y]

    def expand(self, image):
        while self.size+self.x < len(image) and self.size+self.y < len(image[0]):
            x_ok = (image[self.x+self.size,self.y]==self.color).all()
            y_ok = (image[self.x,self.y+self.size]==self.color).all()
            d_ok = (image[self.x+self.size,self.y+self.size]==self.color).all()
            if not (x_ok and y_ok and d_ok):
                break
            self.size +=1
            
    def draw_big(self,image):
        for x in range(0,10):
            for y in range(0,10):
                image[self.x+x,self.y+y] = [0,0,255]

    
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

def find_gray_dots_simple(image):
    squares = []
    for y in range(50,400,20):
        for x in range(120,400,20):
            if is_grey(image[x,y]):
                squares.append(Square(x,y,image[x,y]))           

    return squares

def mouse_left(x,y):
    pyautogui.click(x,y)

def save_image(image, filename="image.png"):
    cv2.imwrite(filename, image)

def main():
    image = screenshot()
    squares = find_gray_dots(image)

    for s in squares:
        s.move_dot(image)

    for i, s1 in enumerate(squares[:]):
        for j,s2 in enumerate(squares[:], start = i):
            if s1.get_position() == s2.get_position() and s1 != s2:
                print(s1,s2)
                squares.remove(s2)
                print("remove",i,j)

    # for s in squares:
    #     print(s.get_position())

    # for i,s1 in enumerate(squares[:]):
    #     for j, s2 in enumerate(squares[:], start=i):
    #         if s1 != s2 and s1.get_position() == s2.get_position():
    #             print("remove",i,j)
    #             squares.remove(s2)

    # for s1 in squares:
    #     s1.expand(image)

    # for i,s in enumerate(squares[:]):
    #     if s.size < 4:
    #         squares.remove(s)

    for s in squares:
        #if (s.size == 22): continue
        s.paint_square(image)

    print(len(squares))
    save_image(image)

class Test:
    """test"""
    def __init__(self, t):
        self.t = t

def test():
    list1 = []
    for x in range(4):
        list1.append(Test(x))
        list1.append(Test(x))
    
    for i, x in enumerate(list1):
        print("x",i,x.t)
        for j,y in enumerate(list1[i:]):
            print("y",j,y.t)
            print("E",x.t,y.t,x,y)
            if x != y and x.t == y.t:
                list1.remove(y)
                print("remove")
    
    for i in list1:
        print(i.t)
    
    


if __name__ == '__main__':
    #main()
    test()