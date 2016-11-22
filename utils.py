import numpy as np
from random import randint

def getColorClass(color):
    ranges = [1, 64, 128, 192, 256]
    for c in range(4):
        l = ranges[c] - 1
        r = ranges[c + 1]
        if(color >= l and color < r):
            return c
    return 0

def getColorClasses(image=None):
    if(image is None):
        print("No Image data")
        return
    max_rows        = image.shape[0]
    max_cols        = image.shape[1]
    classes         = np.zeros(image.shape, np.int8)
    for row in range(max_rows):
        for col in range(max_cols):
            classes[row,col] = getColorClass(image[row,col])
    return classes

def inBounds(row=0, col=0, max_rows=0, max_cols=0):
    return row>=0 and row<max_rows and col >=0 and col < max_cols

def showImage(title='Image', image=None):
    if(image is None):
        print('Error no image data')
        return
    cv2.imshow(title,image)
    cv2.waitKey(0)

def applyLabelColors(labels=None, colors=None, max_rows=None, max_cols=None):
        result_image = np.zeros((max_rows,max_cols,3), np.uint8)
        for row in range(max_rows):
            for col in range(max_cols):
                result_image[row,col] = colors[labels[row,col]%2000]
        return result_image

def generateRandomColors(limit=0):
    colors = []
    for i in range(limit):
        colors.append((randint(0,255),randint(0,255),randint(0,255)))
    return colors
