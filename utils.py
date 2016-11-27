import cv2
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

#filling the image with colors according to labels
def applyLabelColors(labels=None, colors=None, max_rows=None, max_cols=None):
        result_image = np.zeros((max_rows,max_cols,3), np.uint8)
        length       = len(colors)
        for row in range(max_rows):
            for col in range(max_cols):
                result_image[row,col] = colors[labels[row,col]%length]
        return result_image

def generateRandomColors(limit=0):
    colors = []
    for i in range(limit):
        colors.append((randint(0,255),randint(0,255),randint(0,255)))
    return colors

#return True if rect1 is inside rect2 or vice versa
def interHorz(rect1=None, rect2=None):
    X1 = rect1[0]
    W1 = rect1[2]

    X2 = rect2[0]
    W2 = rect2[2]

    if (X1+W1<X2 or X2+W2<X1):
        return False
    else:
        return True

def findRectArea(rect=None):
    W = rect[2]
    H = rect[3]
    return H * W

#Calculates the Mean Squared Error between 2 images
def mse(imageA, imageB):
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
