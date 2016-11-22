import cv2
import numpy as np
from matplotlib import pyplot as pltd
from utils import inBounds, newR, newC
from ccbin import connectedComponentsBin

def showImage(title='Image', image=None):
    if(image is None):
        print('Error no image data')
        return
    cv2.imshow(title,image)
    cv2.waitKey(0)

img = cv2.imread('images/L1.jpg',0)
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #CONVERTING L1.jpg TO BINARY

max_rows      = thresh1.shape[0]
max_cols      = thresh1.shape[1]

#filling the image with colors according to labels
labels = connectedComponentsBin(thresh1)
for row in range(max_rows):
    for col in range(max_cols):
        thresh1[row,col] = labels[row,col] + 100

showImage('Image Binary',thresh1)
